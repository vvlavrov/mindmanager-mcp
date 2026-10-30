"""MindManager FastMCP Server.

Exposes a comprehensive suite of Model Context Protocol (MCP) tools for programmatically
creating and managing mind maps, task roadmaps, and diagrams in Mindjet MindManager.
"""

from typing import Optional, List
from fastmcp import FastMCP
from src.com_bridge import MindManagerBridge

# Initialize FastMCP Server
mcp = FastMCP("MindManager MCP")
bridge = MindManagerBridge()


@mcp.tool
def create_map(title: str = "AI-Trading Roadmap") -> dict:
    """Create a new mind map document with the specified central topic title."""
    return bridge.create_document(title=title)


@mcp.tool
def save_map(file_path: Optional[str] = None) -> dict:
    """Save the active MindManager map. If file_path is given, saves as that file (.mmap)."""
    return bridge.save_active_document(file_path=file_path)


@mcp.tool
def get_map_tree() -> dict:
    """Retrieve the full hierarchical structure of the active map, including tasks, notes, and topics."""
    return bridge.get_map_tree()


@mcp.tool
def add_subtopic(
    parent_topic: str,
    title: str,
    notes: Optional[str] = None,
    complete_percent: Optional[int] = None,
    priority: Optional[int] = None,
    shape: Optional[str] = None,
    fill_color: Optional[str] = None,
    text_color: Optional[str] = None,
    line_color: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> dict:
    """
    Add a new subtopic branch to a specified parent topic (by title or GUID).

    Parameters:
    - parent_topic: Text title or GUID of the parent topic (use central topic title if root).
    - title: Text title for the new subtopic.
    - notes: Detailed text description to store in the topic's Notes tab.
    - complete_percent: Task completion percentage (0 to 100).
    - priority: Task priority from 1 (highest/urgent) to 9 (lowest).
    - shape: Shape name, e.g. 'ROUNDED_RECTANGLE', 'RECTANGLE', 'CAPSULE', 'HEXAGON', 'DATABASE', 'DIAMOND'.
    - fill_color: Background HEX color, e.g. '#E6F2FF'.
    - text_color: Font HEX color, e.g. '#003366'.
    - line_color: Line HEX color, e.g. '#0078D7'.
    - tags: List of category tags.
    """
    return bridge.add_subtopic(
        parent_identifier=parent_topic,
        title=title,
        notes=notes,
        complete_percent=complete_percent,
        priority=priority,
        shape=shape,
        fill_color=fill_color,
        text_color=text_color,
        line_color=line_color,
        tags=tags,
    )


@mcp.tool
def add_floating_topic(title: str) -> dict:
    """Add an independent floating topic anywhere on the active map canvas."""
    return bridge.add_floating_topic(title=title)


@mcp.tool
def add_callout(topic: str, text: str) -> dict:
    """Add a callout (сноска/выноска) attached to a specific topic."""
    return bridge.add_callout(topic_identifier=topic, text=text)


@mcp.tool
def set_task_info(
    topic: str,
    complete_percent: Optional[int] = None,
    priority: Optional[int] = None,
    due_date: Optional[str] = None,
    start_date: Optional[str] = None,
    resources: Optional[List[str]] = None,
) -> dict:
    """
    Update project task attributes for a topic card.

    Parameters:
    - topic: Title or GUID of the topic.
    - complete_percent: 0 (not started), 25, 50, 75, 100 (done).
    - priority: Priority level from 1 (urgent) to 9 (low).
    - due_date: Deadline date in 'YYYY-MM-DD' format.
    - start_date: Start date in 'YYYY-MM-DD' format.
    - resources: List of assigned people, teams, or AI agents (e.g. ['Claude', 'Backtester']).
    """
    return bridge.set_task(
        topic_identifier=topic,
        complete_percent=complete_percent,
        priority=priority,
        due_date=due_date,
        start_date=start_date,
        resources=resources,
    )


@mcp.tool
def set_topic_notes(topic: str, notes: str) -> dict:
    """Set or update the detailed text description (Topic Notes) for a topic card."""
    return bridge.set_topic_notes(topic_identifier=topic, notes_text=notes)


@mcp.tool
def add_comment(topic: str, comment: str, author: str = "Max AI") -> dict:
    """Add a review comment to a topic with author name and current timestamp."""
    return bridge.add_comment(topic_identifier=topic, comment_text=comment, author=author)


@mcp.tool
def set_topic_style(
    topic: str,
    shape: Optional[str] = None,
    fill_color: Optional[str] = None,
    text_color: Optional[str] = None,
    line_color: Optional[str] = None,
    bold: Optional[bool] = None,
    font_size: Optional[float] = None,
) -> dict:
    """
    Customize the visual formatting, colors, and shape of a topic card.

    Parameters:
    - topic: Title or GUID of the topic.
    - shape: 'ROUNDED_RECTANGLE', 'RECTANGLE', 'CAPSULE', 'HEXAGON', 'DATABASE', 'DIAMOND', 'OVAL', 'OCTAGON'.
    - fill_color: HEX color for background (e.g. '#D4EDDA' for light green).
    - text_color: HEX color for text font (e.g. '#155724').
    - line_color: HEX color for border line.
    - bold: True for bold text.
    - font_size: Font size in points (e.g. 10, 12, 14).
    """
    return bridge.set_style(
        topic_identifier=topic,
        shape=shape,
        fill_color=fill_color,
        text_color=text_color,
        line_color=line_color,
        bold=bold,
        font_size=font_size,
    )


@mcp.tool
def add_boundary(
    topic: str,
    shape: str = "RECTANGLE",
    fill_color: Optional[str] = None,
    line_color: Optional[str] = None,
    line_style: str = "SOLID",
) -> dict:
    """
    Create a colored visual boundary box around a topic branch and its subtopics.

    Parameters:
    - topic: Root topic of the group to enclose.
    - shape: 'RECTANGLE', 'CURVED_RECTANGLE', 'WAVES', 'SCALLOPS', 'ZIGZAG', 'LINES'.
    - fill_color: Semi-transparent background HEX color.
    - line_color: Border line HEX color.
    - line_style: 'SOLID', 'DASH', 'ROUND_DOT', 'SQUARE_DOT', 'DASH_DOT'.
    """
    return bridge.add_boundary(
        topic_identifier=topic,
        shape=shape,
        fill_color=fill_color,
        line_color=line_color,
        line_style=line_style,
    )


@mcp.tool
def add_relationship(
    source_topic: str,
    target_topic: str,
    label: str = "",
    line_color: str = "#FF4500",
    line_style: str = "SOLID",
) -> dict:
    """
    Create an arrow / relationship link connecting two topics with an optional label.

    Parameters:
    - source_topic: Origin topic title or GUID.
    - target_topic: Destination topic title or GUID.
    - label: Text label shown on the relationship line (e.g. 'Feeds data to', 'Blocks').
    - line_color: HEX color for the arrow (default: '#FF4500').
    - line_style: 'SOLID', 'DASH', 'DASH_DOT'.
    """
    return bridge.add_relationship(
        source_identifier=source_topic,
        target_identifier=target_topic,
        label=label,
        line_color=line_color,
        line_style=line_style,
    )


@mcp.tool
def add_icon(topic: str, icon_name: str) -> dict:
    """
    Add a stock icon marker to a topic.

    Common icons: 'ROCKET', 'CHECK', 'EXCLAMATION_MARK', 'QUESTION_MARK',
    'FLAG_RED', 'FLAG_GREEN', 'FLAG_YELLOW', 'BOMB', 'DOLLAR', 'CLOCK',
    'CALENDAR', 'LIGHTBULB', 'THUMBS_UP', 'STOP', 'KEY'.
    """
    return bridge.add_icon(topic_identifier=topic, icon_name=icon_name)


@mcp.tool
def add_hyperlink(topic: str, url: str, title: str = "") -> dict:
    """Add a clickable URL or local file path link to a topic."""
    return bridge.add_hyperlink(topic_identifier=topic, url=url, title=title)


@mcp.tool
def delete_topic(topic: str) -> dict:
    """Delete a topic branch and all its descendants from the active map."""
    return bridge.delete_topic(topic_identifier=topic)


if __name__ == "__main__":
    mcp.run()
