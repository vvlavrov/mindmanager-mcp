"""COM Automation Bridge for Mindjet MindManager."""

from datetime import datetime
import os
import re
import pywintypes
import win32com.client
from typing import Any, Optional

from src.constants import (
    TopicShape,
    BoundaryShape,
    LineDashStyle,
    TaskPriority,
    StockIcon,
    hex_to_argb,
)


class MindManagerBridge:
    """Encapsulates MindManager COM automation interactions."""

    def __init__(self):
        self._app = None
        self._doc = None

    def get_app(self):
        """Ensure connection to running MindManager application."""
        import pythoncom
        from win32com.client import gencache
        pythoncom.CoInitialize()
        app = gencache.EnsureDispatch("Mindmanager.Application")
        app.Visible = True
        return app

    def get_active_doc(self):
        """Return the active document or create one if none open."""
        app = self.get_app()
        app.Visible = True
        if app.Documents.Count == 0:
            return app.Documents.Add(True)
        return app.ActiveDocument

    def create_document(self, title: str = "New Map") -> dict:
        """Create a new MindManager map document with given central topic title."""
        app = self.get_app()
        app.Visible = True
        self._doc = app.Documents.Add(True)
        ct = self._doc.CentralTopic
        ct.Text = title
        return {
            "status": "success",
            "document_name": self._doc.Name,
            "central_topic": ct.Text,
            "central_topic_guid": ct.Guid,
        }

    def save_active_document(self, file_path: Optional[str] = None) -> dict:
        """Save the active document to disk."""
        doc = self.get_active_doc()
        if file_path:
            norm_path = os.path.abspath(file_path)
            doc.SaveAs(norm_path)
            return {"status": "saved", "path": norm_path}
        else:
            doc.Save()
            return {"status": "saved", "path": getattr(doc, "FullName", doc.Name)}

    def find_topic(self, identifier: str):
        """
        Find a topic by GUID or exact/case-insensitive text match.
        Searches recursively from CentralTopic and FloatingTopics.
        """
        doc = self.get_active_doc()
        if not identifier:
            return doc.CentralTopic

        # Try GUID direct lookup first if identifier looks like a GUID
        if re.match(r"^\{?[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}?$", identifier.strip()):
            try:
                topic = doc.FindByGuid(identifier.strip())
                if topic is not None and getattr(topic, "IsValid", True):
                    return topic
            except Exception:
                pass

        clean_target = identifier.replace("\r", "").replace("\n", "").strip().lower()

        # Breadth-first search across all trees starting from CentralTopic and FloatingTopics
        queue = [doc.CentralTopic]
        try:
            for ft in doc.FloatingTopics:
                queue.append(ft)
        except Exception:
            pass

        while queue:
            curr = queue.pop(0)
            clean_curr = getattr(curr, "Text", "").replace("\r", "").replace("\n", "").strip().lower()
            if clean_curr == clean_target:
                return curr
            try:
                for child in curr.AllSubTopics:
                    queue.append(child)
            except Exception:
                pass

        raise ValueError(f"Topic with identifier '{identifier}' not found in active map.")

    def add_subtopic(
        self,
        parent_identifier: str,
        title: str,
        notes: Optional[str] = None,
        complete_percent: Optional[int] = None,
        priority: Optional[int] = None,
        shape: Optional[str] = None,
        fill_color: Optional[str] = None,
        text_color: Optional[str] = None,
        line_color: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> dict:
        """Add a subtopic to a parent topic with optional metadata and styling."""
        parent = self.find_topic(parent_identifier)
        sub = getattr(parent, "AddSubTopic", getattr(parent, "AddSubtopic", None))(title)

        if notes:
            sub.Notes.Text = notes

        if complete_percent is not None or priority is not None:
            task = sub.Task
            if complete_percent is not None:
                task.Complete = max(0, min(100, int(complete_percent)))
            if priority is not None and 0 <= priority <= 9:
                task.Priority = int(priority)

        if fill_color:
            a, r, g, b = hex_to_argb(fill_color)
            sub.FillColor.SetARGB(a, r, g, b)

        if text_color:
            a, r, g, b = hex_to_argb(text_color)
            sub.TextColor.SetARGB(a, r, g, b)

        if line_color:
            a, r, g, b = hex_to_argb(line_color)
            sub.LineColor.SetARGB(a, r, g, b)

        if shape:
            shape_enum = getattr(TopicShape, shape.upper(), None)
            if shape_enum:
                sub.Shape.SetTypes(int(shape_enum), 1, 1)

        if tags:
            for t in tags:
                try:
                    sub.TextLabels.AddTextLabelFromGroup(t, "", True)
                except Exception:
                    pass

        return {
            "status": "created",
            "title": sub.Text,
            "guid": sub.Guid,
            "parent": parent.Text,
            "is_done": sub.Task.IsDone,
            "complete": sub.Task.Complete,
            "priority": sub.Task.Priority,
        }

    def add_floating_topic(self, title: str) -> dict:
        """Add a floating topic on the active map canvas."""
        doc = self.get_active_doc()
        ft = doc.FloatingTopics.Add(title)
        return {
            "status": "created",
            "title": ft.Text,
            "guid": ft.Guid,
            "type": "floating_topic",
        }

    def add_callout(self, topic_identifier: str, text: str) -> dict:
        """Add a callout note (сноска-выноска) attached to a topic."""
        topic = self.find_topic(topic_identifier)
        callout = topic.CalloutTopics.Add("")
        callout.Text = text
        return {
            "status": "created",
            "text": callout.Text,
            "attached_to": topic.Text,
            "guid": callout.Guid,
        }

    def set_task(
        self,
        topic_identifier: str,
        complete_percent: Optional[int] = None,
        priority: Optional[int] = None,
        due_date: Optional[str] = None,
        start_date: Optional[str] = None,
        resources: Optional[list[str]] = None,
    ) -> dict:
        """Update task properties for a topic."""
        topic = self.find_topic(topic_identifier)
        task = topic.Task

        if complete_percent is not None:
            task.Complete = max(0, min(100, int(complete_percent)))

        if priority is not None:
            task.Priority = max(0, min(9, int(priority)))

        if due_date:
            try:
                dt = datetime.strptime(due_date, "%Y-%m-%d")
                task.DueDate = pywintypes.Time(dt)
            except Exception as e:
                raise ValueError(f"Invalid due_date format, expected YYYY-MM-DD: {e}")

        if start_date:
            try:
                dt = datetime.strptime(start_date, "%Y-%m-%d")
                task.StartDate = pywintypes.Time(dt)
            except Exception as e:
                raise ValueError(f"Invalid start_date format, expected YYYY-MM-DD: {e}")

        if resources:
            for r in resources:
                try:
                    task.Resources.Add(r)
                except Exception:
                    pass

        return {
            "topic": topic.Text,
            "complete": task.Complete,
            "is_done": task.IsDone,
            "priority": task.Priority,
            "has_due_date": getattr(task, "HasDueDate", False),
        }

    def set_topic_notes(self, topic_identifier: str, notes_text: str) -> dict:
        """Set description / notes text for a topic."""
        topic = self.find_topic(topic_identifier)
        topic.Notes.Text = notes_text
        return {"topic": topic.Text, "notes_length": len(notes_text)}

    def add_comment(self, topic_identifier: str, comment_text: str, author: str = "Max AI") -> dict:
        """Add a review comment to a topic."""
        topic = self.find_topic(topic_identifier)
        now = pywintypes.Time(datetime.now())
        comment = topic.ReviewComments.Add(comment_text, author, now)
        return {
            "topic": topic.Text,
            "comment": comment.Text,
            "author": comment.AuthorName,
            "status": "added",
        }

    def set_style(
        self,
        topic_identifier: str,
        shape: Optional[str] = None,
        fill_color: Optional[str] = None,
        text_color: Optional[str] = None,
        line_color: Optional[str] = None,
        bold: Optional[bool] = None,
        font_size: Optional[float] = None,
    ) -> dict:
        """Update visual formatting of a topic."""
        topic = self.find_topic(topic_identifier)

        if shape:
            shape_enum = getattr(TopicShape, shape.upper(), None)
            if shape_enum:
                topic.Shape.SetTypes(int(shape_enum), 1, 1)

        if fill_color:
            a, r, g, b = hex_to_argb(fill_color)
            topic.FillColor.SetARGB(a, r, g, b)

        if text_color:
            a, r, g, b = hex_to_argb(text_color)
            topic.TextColor.SetARGB(a, r, g, b)

        if line_color:
            a, r, g, b = hex_to_argb(line_color)
            topic.LineColor.SetARGB(a, r, g, b)

        if bold is not None:
            topic.Font.Bold = bold

        if font_size is not None:
            topic.Font.Size = font_size

        return {"topic": topic.Text, "status": "style_updated"}

    def add_boundary(
        self,
        topic_identifier: str,
        shape: str = "RECTANGLE",
        fill_color: Optional[str] = None,
        line_color: Optional[str] = None,
        line_style: str = "SOLID",
    ) -> dict:
        """Create a visual boundary box around a topic and its children."""
        topic = self.find_topic(topic_identifier)
        boundary = topic.CreateBoundary()

        shape_enum = getattr(BoundaryShape, shape.upper(), BoundaryShape.RECTANGLE)
        boundary.Shape = int(shape_enum)

        dash_enum = getattr(LineDashStyle, line_style.upper(), LineDashStyle.SOLID)
        boundary.LineDashStyle = int(dash_enum)

        if fill_color:
            a, r, g, b = hex_to_argb(fill_color)
            boundary.FillColor.SetARGB(a, r, g, b)

        if line_color:
            a, r, g, b = hex_to_argb(line_color)
            boundary.LineColor.SetARGB(a, r, g, b)

        return {
            "topic": topic.Text,
            "boundary_shape": boundary.Shape,
            "status": "boundary_created",
        }

    def add_relationship(
        self,
        source_identifier: str,
        target_identifier: str,
        label: str = "",
        line_color: Optional[str] = "#FF4500",
        line_style: str = "SOLID",
    ) -> dict:
        """Add an arrow / relationship line connecting two topics."""
        source = self.find_topic(source_identifier)
        target = self.find_topic(target_identifier)

        rel = source.Relationships.AddToTopic(target, label)
        if line_color:
            a, r, g, b = hex_to_argb(line_color)
            rel.LineColor.SetARGB(a, r, g, b)

        dash_enum = getattr(LineDashStyle, line_style.upper(), LineDashStyle.SOLID)
        rel.LineDashStyle = int(dash_enum)

        return {
            "source": source.Text,
            "target": target.Text,
            "label": label,
            "status": "relationship_created",
        }

    def add_icon(self, topic_identifier: str, icon_name: str) -> dict:
        """Add a stock icon marker to a topic."""
        topic = self.find_topic(topic_identifier)
        icon_enum = getattr(StockIcon, icon_name.upper(), None)
        if not icon_enum:
            raise ValueError(f"Unknown stock icon '{icon_name}'.")
        topic.UserIcons.AddStockIcon(int(icon_enum))
        return {"topic": topic.Text, "icon": icon_name, "status": "icon_added"}

    def add_hyperlink(self, topic_identifier: str, url: str, title: str = "") -> dict:
        """Add a hyperlink or local file link to a topic."""
        topic = self.find_topic(topic_identifier)
        link = topic.Hyperlinks.AddHyperlink(url)
        if title:
            link.Title = title
        return {"topic": topic.Text, "url": url, "status": "hyperlink_added"}

    def delete_topic(self, topic_identifier: str) -> dict:
        """Delete a topic and its children."""
        topic = self.find_topic(topic_identifier)
        title = topic.Text
        topic.Delete()
        return {"status": "deleted", "title": title}

    def get_map_tree(self) -> dict:
        """Extract the full map hierarchy into a structured JSON dictionary."""
        doc = self.get_active_doc()
        ct = doc.CentralTopic

        def serialize_topic(t):
            data = {
                "title": t.Text,
                "guid": t.Guid,
                "level": getattr(t, "Level", 0),
            }

            # Task info
            try:
                task = t.Task
                if not task.IsEmpty:
                    data["task"] = {
                        "complete": task.Complete,
                        "is_done": task.IsDone,
                        "priority": task.Priority,
                    }
            except Exception:
                pass

            # Notes
            try:
                notes = t.Notes
                if notes and not notes.IsEmpty and notes.Text:
                    data["notes"] = notes.Text
            except Exception:
                pass

            # Subtopics
            subtopics = []
            try:
                for sub in t.AllSubTopics:
                    subtopics.append(serialize_topic(sub))
            except Exception:
                pass
            data["subtopics"] = subtopics
            return data

        return {
            "document_name": doc.Name,
            "central_topic": serialize_topic(ct),
        }
