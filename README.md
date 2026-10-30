# MindManager MCP Server 🚀

A comprehensive **Model Context Protocol (MCP)** server that enables Large Language Models (LLMs) like Claude, Gemini, and Cursor to programmatically create, manage, style, and query mind maps and task roadmaps directly inside **Mindjet MindManager** on Windows via COM automation.

---

## 🌟 Key Capabilities

* **Map & Branch Management:**
  * Create new maps with custom central topics (`create_map`).
  * Add subtopics of any depth (`add_subtopic`).
  * Add independent floating topics (`add_floating_topic`) and callouts (`add_callout`).
  * Inspect the full hierarchy as JSON / tree (`get_map_tree`).
  * Delete branches (`delete_topic`).
* **Task & Project Management (AI-Trading Roadmap):**
  * Track completion percentage: `0%`, `25%`, `50%`, `75%`, `100%` (`IsDone` flag).
  * Priority levels: 1 (Urgent/Critical) to 9 (Low).
  * Milestones, start dates, due dates / deadlines.
  * Assign resources (developers, AI agents, sub-systems).
* **Styling & Visual Design:**
  * 15 topic shapes: `ROUNDED_RECTANGLE`, `RECTANGLE`, `CAPSULE`, `HEXAGON`, `DATABASE`, `DIAMOND`, etc.
  * Custom background fill colors, text colors, line colors (HEX format).
  * Font sizing and bold styling.
* **Boundaries & Grouping:**
  * Create colored visual boundaries (`add_boundary`) around entire sub-trees.
  * Multiple boundary shapes (`RECTANGLE`, `CURVED_RECTANGLE`, `WAVES`, etc.) and line dash styles.
* **Relationships & Dependencies:**
  * Draw directional arrows between any two topics with labels and custom colors (`add_relationship`).
* **Notes, Comments & Markers:**
  * Rich descriptions and notes for each topic (`set_topic_notes`).
  * Review comments with author stamps and timestamps (`add_comment`).
  * 70+ stock icons (flags, rocket 🚀, warning ⚠️, checkmark ✅, dollar 💵, etc.).
  * Hyperlinks to files or web URLs (`add_hyperlink`).

---

## 🛠 Installation & Local Setup

### 1. Requirements
* Windows OS
* Mindjet MindManager (tested on MindManager 2020 / v20.1+)
* Python 3.11+

### 2. Setup Virtual Environment
```bash
cd d:\Dev\mindmanager-mcp
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

---

## 🔌 Connecting to MCP Clients

### 1. Antigravity IDE
Add the server entry to `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "mindmanager": {
      "command": "d:\\Dev\\mindmanager-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "src.server"]
    }
  }
}
```

### 2. Claude Desktop
Add the server entry to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mindmanager": {
      "command": "d:\\Dev\\mindmanager-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "src.server"]
    }
  }
}
```

---

## 📜 License
MIT License. Created by Viacheslav Lavrov.
