"""Prompt engineering for the Planner Agent.

Every prompt asks for ONE JSON object in a fixed shape so the frontend can
render each part of the blueprint reliably.
"""
import json

SYSTEM = (
    "You are the Planner Agent inside the AI Project Builder. You turn a "
    "high-level software idea into a practical, beginner-friendly project plan. "
    "Be concrete and realistic about scope and time. Respond with a single valid "
    "JSON object and nothing else: no markdown fences, no commentary."
)

OPTIONS_SHAPE = """{
  "options": [
    {
      "id": "A",
      "title": "short name for this approach",
      "tagline": "one sentence describing the approach",
      "why_choose": "2-3 sentences on why this option suits the stated purpose",
      "best_for": "the situation or team this is best for",
      "difficulty": "Beginner | Intermediate | Advanced",
      "estimated_time": "e.g. 24 hours, 2 weeks, 2 months",
      "suggested_stack": ["tech 1", "tech 2", "tech 3"],
      "key_features": ["feature 1", "feature 2", "feature 3"]
    }
  ]
}"""

BLUEPRINT_SHAPE = """{
  "project_name": "short project name",
  "one_line_summary": "what the project does and for whom",
  "features": [
    {"name": "feature name", "priority": "Must | Should | Nice", "description": "one sentence"}
  ],
  "non_functional_requirements": ["e.g. works on mobile browsers", "..."],
  "tech_stack": [
    {"layer": "Frontend | Backend | Database | AI | Hosting | ...", "choice": "technology", "reason": "why it fits"}
  ],
  "folder_structure": "a text tree, one path per line, using indentation and / for folders",
  "database_schema": [
    {
      "table": "table_name",
      "purpose": "what it stores",
      "columns": [{"name": "id", "type": "INTEGER PK", "notes": "auto increment"}]
    }
  ],
  "roadmap": [
    {"phase": "phase name", "goal": "what is done at the end", "duration": "e.g. 2 hours", "tasks": ["task 1", "task 2"]}
  ],
  "starter_code": [
    {"path": "relative/file/path.py", "language": "python", "description": "what this file does", "code": "file contents"}
  ]
}"""


def options_prompt(idea: str, purpose: str) -> str:
    return (
        "A user wants to build this project.\n\n"
        f"Idea: {idea}\n"
        f"Purpose: {purpose}\n\n"
        "Propose exactly 3 distinct ways to build it, tailored to the purpose. "
        "Think about the time available, how the project will be judged or used, "
        "and the skill level typical for that purpose. The options must differ in "
        "scope, approach or technology, not just in wording. Use ids A, B and C.\n\n"
        "Return JSON in exactly this shape:\n" + OPTIONS_SHAPE
    )


def blueprint_prompt(idea: str, purpose: str, option: dict) -> str:
    return (
        "Create a complete project blueprint.\n\n"
        f"Idea: {idea}\n"
        f"Purpose: {purpose}\n"
        f"Chosen approach: {json.dumps(option, ensure_ascii=False)}\n\n"
        "Rules:\n"
        "- 5 to 8 features. Mark the first working version as Must, the rest Should or Nice.\n"
        "- Tech stack must match the chosen approach.\n"
        "- Folder structure must match the starter code paths.\n"
        "- Database schema: realistic tables with columns, types and notes. "
        "Return an empty list if the project needs no database.\n"
        "- Roadmap: 4 to 5 phases in build order, 3 to 6 tasks each.\n"
        "- Starter code: 3 to 5 files that form a runnable skeleton. Keep each file "
        "under 60 lines, with short comments. Prefer working minimal code over completeness.\n"
        "- Write for a beginner who has never planned a project before.\n\n"
        "Return JSON in exactly this shape:\n" + BLUEPRINT_SHAPE
    )
