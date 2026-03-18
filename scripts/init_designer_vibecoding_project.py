#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def make_agents_md(project_name: str) -> str:
    return f"""# AGENTS.md

## Purpose
- Keep this project usable, collaborative, and easy to hand off.
- Use the workflow files as the source of truth instead of chat memory.

## Working Rules
- Start small, verify fast, expand later.
- Do not change scope silently.
- Write plans for tasks with 3+ steps or any architecture decision.
- Do not mark work done without runnable evidence.

## Must-Read Order
1. `AGENTS.md`
2. `agent-context/current-workflow.md`
3. `project-management/active-sprint.md`

## Project
- Name: `{project_name}`
- This repo was initialized from `designer-vibecoding-starter`.
"""


def make_current_workflow(workflow_id: str) -> str:
    owner = "claude+codex" if workflow_id == "claude-planner-codex-builder" else "codex"
    return f"""# Current Workflow

workflow_id: {workflow_id}
updated_at: {today()}
owner: {owner}

## Start Here
1. `/AGENTS.md`
2. `/agent-context/current-workflow.md`
3. `/agent-context/default-context.md`
4. `/project-management/active-sprint.md`
5. `/project-management/backlog.md`

## Rule
- Only one workflow is active at a time.
- If switching workflow, update this file first.
"""


def make_default_context(path_mode: str, openclaw_enabled: bool) -> str:
    path_line = (
        "Design-driven path: design analysis -> PRD -> product check -> build -> test -> design QA"
        if path_mode == "design-driven"
        else "Zero-to-one path: intent -> planning -> PRD -> spec/todo -> build -> test -> review"
    )
    remote_line = (
        "OpenClaw is enabled for optional background execution."
        if openclaw_enabled
        else "OpenClaw is not enabled in this project by default."
    )
    return f"""# Default Context

## Delivery Path
- {path_line}

## Collaboration Modes
- `claude-planner-codex-builder`
- `codex-fullstack-workflow`
- {remote_line}

## Shared Inputs
- `.agent/handoff.json` is the single task handoff source.
- `.agent/status.json` is the single execution status source.
- `scripts/agent_run.sh` is the single execution entry.
"""


def make_workflow_selector() -> str:
    return """# Workflow Selector

## Available modes

1. `Claude Code + Codex`
2. `Codex fullstack`
3. `OpenClaw` background execution (optional overlay)

## Example Chinese intents

- `切换到 Claude 规划 + Codex 开发`
- `跟我用 Codex 协作链路`
- `开启 OpenClaw 后台执行`
"""


def make_collab_overview(path_mode: str, openclaw_enabled: bool) -> str:
    path_label = "基于设计稿" if path_mode == "design-driven" else "0-1 无设计稿"
    openclaw_line = "Enabled" if openclaw_enabled else "Disabled"
    return f"""# Collaboration Workflows Overview

## Current delivery path
- {path_label}

## Modes
- `claude-planner-codex-builder`
- `codex-fullstack-workflow`
- `OpenClaw`: {openclaw_line}

## Single sources of truth
- `agent-context/current-workflow.md`
- `.agent/handoff.json`
- `.agent/status.json`
- `scripts/agent_run.sh`
"""


def make_workflow_doc(name: str, summary: str) -> str:
    return f"""# {name}

## Summary
- {summary}

## Steps
1. Clarify the task
2. Write or refine the spec/todo
3. Fill `.agent/handoff.json`
4. Execute with `scripts/agent_run.sh`
5. Verify and record results
"""


def make_agent_roles() -> str:
    return """# Agent Roles

- `project-manager`: clarify scope and track status
- `architect`: define implementation structure
- `engineer`: implement the change
- `tester`: run validation
- `reviewer`: check risk and regressions
- `design-analyst`: translate design into implementation constraints
"""


def make_design_file(title: str, active: bool, body: str) -> str:
    status = "active" if active else "optional"
    return f"""# {title}

status: {status}

{body}
"""


def make_active_prd(project_name: str, path_mode: str) -> str:
    flow = (
        "Design analysis -> design contract -> PRD slices -> implementation -> design QA"
        if path_mode == "design-driven"
        else "Intent clarification -> PRD -> implementation slices -> validation"
    )
    return f"""# Active PRD

## Project
- {project_name}

## Path
- {path_mode}

## Delivery flow
- {flow}

## Current objective
- Replace this section with the first real deliverable.
"""


def make_active_sprint(project_name: str) -> str:
    return f"""# Active Sprint

- Project: {project_name}
- Status: in-progress

## Goal
- Initialize the collaboration system
- Define the first deliverable
- Produce the first executable handoff

## Checklist
- [ ] Confirm scope
- [ ] Fill active PRD
- [ ] Fill tasks/todo.md
- [ ] Create first handoff
- [ ] Run verification
"""


def make_backlog() -> str:
    return """# Backlog

## Now
- [ ] Define the first milestone

## Next
- [ ] Expand PRD slices
- [ ] Add verification cases

## Later
- [ ] Add automation improvements
"""


def make_changelog() -> str:
    return f"""# Changelog

## {today()}
- Project scaffold initialized from `designer-vibecoding-starter`.
"""


def make_todo(path_mode: str) -> str:
    extra = (
        "- [ ] Complete design analysis\n- [ ] Complete design QA"
        if path_mode == "design-driven"
        else "- [ ] Clarify initial product intent\n- [ ] Draft first PRD slice"
    )
    return f"""# Todo

## Current Plan
- [ ] Confirm first milestone
{extra}
- [ ] Create handoff
- [ ] Run verification

## Review
- Pending
"""


def make_lessons() -> str:
    return """# Lessons

- Add repeated corrections and workflow learnings here.
- Review relevant items before starting major work.
"""


def make_handoff() -> str:
    return json.dumps(
        {
            "task_id": "init-first-task",
            "title": "Replace with your first real task",
            "steps": [],
            "test_commands": [],
        },
        ensure_ascii=False,
        indent=2,
    )


def make_status() -> str:
    return json.dumps(
        {"status": "idle", "task_id": "", "updated_at": now_iso()},
        ensure_ascii=False,
        indent=2,
    )


def make_package_json(openclaw_enabled: bool) -> str:
    scripts = {
        "workflow:intent": "bash ./scripts/workflow_intent.sh",
        "validate:handoff": "bash ./scripts/validate_handoff.sh",
        "agent:run": "bash ./scripts/agent_run.sh",
    }
    if openclaw_enabled:
        scripts["openclaw:worker"] = "bash ./scripts/openclaw_worker.sh"
        scripts["openclaw:daemon"] = "bash ./scripts/openclaw_daemon.sh"
    return json.dumps(
        {"name": "designer-vibecoding-template", "private": True, "scripts": scripts},
        ensure_ascii=False,
        indent=2,
    )


WORKFLOW_INTENT_SH = """#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

INTENT="${*:-}"
if [[ -z "$INTENT" ]]; then
  echo "Usage: bash ./scripts/workflow_intent.sh \\"中文意图\\""
  echo "例如："
  echo "  bash ./scripts/workflow_intent.sh \\"切换到 Claude 规划 + Codex 开发\\""
  echo "  bash ./scripts/workflow_intent.sh \\"跟我用 Codex 协作链路\\""
  echo "  bash ./scripts/workflow_intent.sh \\"开启 OpenClaw 后台执行\\""
  exit 1
fi

CURRENT_WORKFLOW="$(sed -n 's/^workflow_id: //p' agent-context/current-workflow.md | head -n 1)"
TARGET_WORKFLOW="$CURRENT_WORKFLOW"
OPENCLAW_ACTION="no-change"
PATH_MODE="no-change"
TARGET_OWNER="$(sed -n 's/^owner: //p' agent-context/current-workflow.md | head -n 1)"
TODAY="$(date +%F)"

# 协作模式识别
if [[ "$INTENT" == *"Claude"* ]] || [[ "$INTENT" == *"Claude 规划"* ]] || [[ "$INTENT" == *"旧协作"* ]]; then
  TARGET_WORKFLOW="claude-planner-codex-builder"
elif [[ "$INTENT" == *"Codex"* ]] || [[ "$INTENT" == *"多 agent"* ]] || [[ "$INTENT" == *"多agent"* ]] || [[ "$INTENT" == *"全流程"* ]]; then
  TARGET_WORKFLOW="codex-fullstack-workflow"
fi

if [[ "$TARGET_WORKFLOW" == "claude-planner-codex-builder" ]]; then
  TARGET_OWNER="claude+codex"
else
  TARGET_OWNER="codex"
fi

# OpenClaw 识别
if [[ "$INTENT" == *"OpenClaw"* ]] || [[ "$INTENT" == *"后台"* ]] || [[ "$INTENT" == *"远程"* ]]; then
  OPENCLAW_ACTION="enable"
fi

# 路径识别
if [[ "$INTENT" == *"有设计稿"* ]] || [[ "$INTENT" == *"设计驱动"* ]] || [[ "$INTENT" == *"design-driven"* ]]; then
  PATH_MODE="design-driven"
elif [[ "$INTENT" == *"没有设计稿"* ]] || [[ "$INTENT" == *"从零开始"* ]] || [[ "$INTENT" == *"zero-to-one"* ]]; then
  PATH_MODE="zero-to-one"
fi

# 如果 workflow 有变化，更新 current-workflow.md
if [[ "$TARGET_WORKFLOW" != "$CURRENT_WORKFLOW" ]]; then
  sed -i.bak "s/^workflow_id: .*/workflow_id: $TARGET_WORKFLOW/" agent-context/current-workflow.md
  sed -i.bak "s/^owner: .*/owner: $TARGET_OWNER/" agent-context/current-workflow.md
  sed -i.bak "s/^updated_at: .*/updated_at: $TODAY/" agent-context/current-workflow.md
  rm -f agent-context/current-workflow.md.bak
  echo "[workflow_intent] switched: $CURRENT_WORKFLOW -> $TARGET_WORKFLOW"
fi

cat <<EOF
{
  "intent": "$INTENT",
  "workflow": "$TARGET_WORKFLOW",
  "workflow_changed": $([ "$TARGET_WORKFLOW" != "$CURRENT_WORKFLOW" ] && echo "true" || echo "false"),
  "openclaw_action": "$OPENCLAW_ACTION",
  "path_mode": "$PATH_MODE"
}
EOF
"""


VALIDATE_HANDOFF_SH = """#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

FILE="${1:-.agent/handoff.json}"
jq -e '.task_id and .title' "$FILE" >/dev/null
echo "handoff ok"
"""


AGENT_RUN_SH = """#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

TASK_ID="$(jq -r '.task_id // "unknown"' .agent/handoff.json)"
echo "{\\"status\\":\\"running\\",\\"task_id\\":\\"$TASK_ID\\"}" > .agent/status.json

# -------------------------------------------------------
# 配置执行命令
# 将下面的 CONFIGURED=false 改为 CONFIGURED=true，
# 并在 run_task() 中填写实际执行命令，例如：
#   codex run --task "$TASK_ID"
#   claude --task "$TASK_ID"
# -------------------------------------------------------
CONFIGURED=false

run_task() {
  # TODO: 替换为实际执行命令
  echo "[agent_run] no command configured"
  return 1
}

if [[ "$CONFIGURED" == "true" ]]; then
  if run_task; then
    echo "{\\"status\\":\\"done\\",\\"task_id\\":\\"$TASK_ID\\"}" > .agent/status.json
    echo "[agent_run] completed: $TASK_ID"
  else
    echo "{\\"status\\":\\"failed\\",\\"task_id\\":\\"$TASK_ID\\"}" > .agent/status.json
    echo "[agent_run] failed: $TASK_ID"
    exit 1
  fi
else
  echo "{\\"status\\":\\"pending-config\\",\\"task_id\\":\\"$TASK_ID\\",\\"error\\":\\"CONFIGURED=false. Edit scripts/agent_run.sh to add your execution command.\\"}" > .agent/status.json
  echo "[agent_run] not configured — set CONFIGURED=true and fill run_task() first."
  exit 1
fi
"""


OPENCLAW_WORKER_SH = """#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

bash ./scripts/validate_handoff.sh
bash ./scripts/agent_run.sh
"""


OPENCLAW_DAEMON_SH = """#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

while true; do
  bash ./scripts/openclaw_worker.sh || true
  sleep "${OPENCLAW_POLL_SECONDS:-30}"
done
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--path-mode", choices=["zero-to-one", "design-driven"], required=True)
    parser.add_argument(
        "--workflow",
        choices=["claude-planner-codex-builder", "codex-fullstack-workflow"],
        required=True,
    )
    parser.add_argument("--openclaw", action="store_true")
    parser.add_argument("--merge", action="store_true", help="Allow scaffolding into a non-empty directory")
    args = parser.parse_args()

    root = Path(args.target).expanduser().resolve()

    if root.exists() and any(root.iterdir()):
        if not args.merge:
            print(
                f"[error] Target directory already exists and is not empty: {root}\n"
                f"        Use --merge to scaffold into an existing directory, or choose a different target."
            )
            raise SystemExit(1)

    root.mkdir(parents=True, exist_ok=True)

    write(root / "AGENTS.md", make_agents_md(args.project_name))
    write(root / "agent-context/current-workflow.md", make_current_workflow(args.workflow))
    write(root / "agent-context/default-context.md", make_default_context(args.path_mode, args.openclaw))

    write(root / "ai-workflows/claude-planner-codex-builder/workflow.md", make_workflow_doc("Claude Planner + Codex Builder", "Claude manages planning/context, Codex handles execution."))
    write(root / "ai-workflows/claude-planner-codex-builder/agent-roles.md", make_agent_roles())
    write(root / "ai-workflows/codex-fullstack-workflow/workflow.md", make_workflow_doc("Codex Fullstack Workflow", "Codex handles planning, build, test, and review by default."))
    write(root / "ai-workflows/codex-fullstack-workflow/agent-roles.md", make_agent_roles())
    write(root / "ai-workflows/shared/handoff-template.md", "# Handoff Template\n\n- Goal\n- Constraints\n- Steps\n- Test commands\n")
    write(root / "ai-workflows/shared/review-template.md", "# Review Template\n\n- Findings\n- Risks\n- Follow-ups\n")
    write(root / "ai-workflows/shared/test-plan-template.md", "# Test Plan Template\n\n- Happy path\n- Edge cases\n- Regression checks\n")

    write(root / "docs/project-entry/workflow-selector.md", make_workflow_selector())
    write(root / "docs/workflows/collaboration-workflows-overview.md", make_collab_overview(args.path_mode, args.openclaw))
    write(root / "docs/product/active-prd.md", make_active_prd(args.project_name, args.path_mode))
    write(root / "docs/design/figma-source.md", make_design_file("Figma Source", args.path_mode == "design-driven", "Add the design source URL or selection details here."))
    write(root / "docs/design/design-analysis.md", make_design_file("Design Analysis", args.path_mode == "design-driven", "Translate layout, components, tokens, and interaction states here."))
    write(root / "docs/design/design-contract.md", make_design_file("Design Contract", args.path_mode == "design-driven", "List component mapping, token constraints, and acceptance rules here."))
    write(root / "docs/design/design-qa.md", make_design_file("Design QA", args.path_mode == "design-driven", "Record final design comparison and issues here."))

    write(root / "project-management/active-sprint.md", make_active_sprint(args.project_name))
    write(root / "project-management/backlog.md", make_backlog())
    write(root / "project-management/changelog.md", make_changelog())

    write(root / "tasks/todo.md", make_todo(args.path_mode))
    write(root / "tasks/lessons.md", make_lessons())
    write(root / ".agent/handoff.json", make_handoff())
    write(root / ".agent/status.json", make_status())
    (root / ".agent/logs").mkdir(parents=True, exist_ok=True)

    write(root / "package.json", make_package_json(args.openclaw))
    write(root / "scripts/workflow_intent.sh", WORKFLOW_INTENT_SH)
    write(root / "scripts/validate_handoff.sh", VALIDATE_HANDOFF_SH)
    write(root / "scripts/agent_run.sh", AGENT_RUN_SH)
    if args.openclaw:
      write(root / "scripts/openclaw_worker.sh", OPENCLAW_WORKER_SH)
      write(root / "scripts/openclaw_daemon.sh", OPENCLAW_DAEMON_SH)

    for script in root.glob("scripts/*.sh"):
        script.chmod(0o755)

    print(json.dumps(
        {
            "target": str(root),
            "project_name": args.project_name,
            "path_mode": args.path_mode,
            "workflow": args.workflow,
            "openclaw": args.openclaw,
            "status": "ok",
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
