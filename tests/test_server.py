"""Integration test for MindManager MCP server."""

import asyncio
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.server import mcp, bridge


def test_mcp_tools_registered():
    """Verify that all expected tools are registered on the FastMCP instance."""
    tools_list = asyncio.run(mcp.list_tools())
    tool_names = [t.name for t in tools_list]
    expected_tools = [
        "create_map",
        "save_map",
        "get_map_tree",
        "add_subtopic",
        "add_floating_topic",
        "add_callout",
        "set_task_info",
        "set_topic_notes",
        "add_comment",
        "set_topic_style",
        "add_boundary",
        "add_relationship",
        "add_icon",
        "add_hyperlink",
        "delete_topic",
    ]
    for tool_name in expected_tools:
        assert tool_name in tool_names, f"Missing tool: {tool_name}"
    print(f"Verified: All {len(expected_tools)} MCP tools are properly registered!")


def test_com_roundtrip():
    """Live smoke test of MindManager COM bridge."""
    res = bridge.create_document("Тестовый Проект MCP")
    assert res["status"] == "success"
    print("Document created:", res["document_name"])

    # Add branch
    branch = bridge.add_subtopic(
        parent_identifier="Тестовый Проект MCP",
        title="Модуль Трейдинга",
        notes="Подробное описание архитектуры",
        complete_percent=50,
        priority=1,
        shape="ROUNDED_RECTANGLE",
        fill_color="#E6F2FF",
        text_color="#003366",
    )
    assert branch["status"] == "created"
    print("Subtopic created:", branch["title"])

    # Add second branch
    branch2 = bridge.add_subtopic(
        parent_identifier="Тестовый Проект MCP",
        title="Модуль Рисков",
        complete_percent=100,
        priority=2,
    )

    # Add relationship
    rel = bridge.add_relationship(
        source_identifier="Модуль Трейдинга",
        target_identifier="Модуль Рисков",
        label="Контроль рисков",
        line_color="#FF4500",
    )
    assert rel["status"] == "relationship_created"
    print("Relationship created:", rel["label"])

    # Add boundary
    boundary = bridge.add_boundary(
        topic_identifier="Модуль Трейдинга",
        shape="RECTANGLE",
        fill_color="#F0F8FF",
        line_color="#0078D7",
    )
    assert boundary["status"] == "boundary_created"
    print("Boundary created around:", boundary["topic"])

    # Add comment
    comm = bridge.add_comment("Модуль Трейдинга", "Проверить задержки API", "Max AI")
    assert comm["status"] == "added"
    print("Comment added:", comm["comment"])

    # Add icon
    icon = bridge.add_icon("Модуль Трейдинга", "ROCKET")
    assert icon["status"] == "icon_added"
    print("Icon added:", icon["icon"])

    # Check tree dump
    tree = bridge.get_map_tree()
    assert "central_topic" in tree
    assert len(tree["central_topic"]["subtopics"]) == 2
    print("Tree dump verified successfully! Subtopics count:", len(tree["central_topic"]["subtopics"]))

    # Clean up test document
    doc = bridge.get_active_doc()
    temp_path = os.path.join(os.environ.get("TEMP", "C:/Temp"), "test_mcp_run.mmap")
    doc.SaveAs(temp_path)
    doc.Close()
    if os.path.exists(temp_path):
        os.remove(temp_path)
    print("Document closed and cleaned up successfully!")


if __name__ == "__main__":
    test_mcp_tools_registered()
    test_com_roundtrip()
    print("\nALL TESTS PASSED SUCCESSFULLY! 🚀")
