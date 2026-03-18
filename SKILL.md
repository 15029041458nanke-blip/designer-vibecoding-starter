---
name: designer-vibecoding-starter
description: Initialize a designer-friendly vibecoding project scaffold with workflow files, collaboration modes, handoff/status infrastructure, and optional OpenClaw helpers. Use when starting a new project from scratch and you want Codex to set up the folder structure, choose between `0-1` or `design-driven` delivery, and configure either a multi-model planning/execution workflow or a single-model multi-agent workflow as the default collaboration mode. 当用户说"帮我搭新项目"、"初始化 vibecoding 项目"、"创建协作脚手架"、"新建 vibecoding 项目"时使用。
---

# Designer Vibecoding Starter

Ask the minimum setup questions, scaffold the project, and leave the user with a working folder structure that already contains the collaboration rules, templates, and execution entry points.

Read `references/template-map.md` for exact question wording, structured form mapping, and path/mode behavior.

## Workflow

### Step 1 — Gather setup choices via AskUserQuestion

Use the `AskUserQuestion` tool to ask all four questions **in a single call** (pass them as an array of up to 4 questions). Do not ask in plain text unless the host does not support the tool.

```json
{
  "questions": [
    {
      "question": "目标目录或项目名称是什么？",
      "header": "项目位置",
      "options": [
        {"label": "填写项目名", "description": "例如 my-app，会在当前目录下创建"},
        {"label": "填写完整路径", "description": "例如 /Users/you/Desktop/my-project"},
        {"label": "当前目录", "description": "直接在当前目录初始化（需明确确认）"}
      ],
      "multiSelect": false
    },
    {
      "question": "项目是否已有设计稿？",
      "header": "开发路径",
      "options": [
        {"label": "有设计稿", "description": "走 design-driven：生成设计分析、设计约束、Design QA 文件"},
        {"label": "没有设计稿", "description": "走 zero-to-one：从意图澄清 → PRD → 实现开始"}
      ],
      "multiSelect": false
    },
    {
      "question": "默认协作模式选哪个？",
      "header": "协作模式",
      "options": [
        {"label": "多模型协作", "description": "一个模型负责规划/上下文，另一个负责执行（如 Claude + Codex）"},
        {"label": "单模型多角色", "description": "由一个模型拆成 PM/架构师/工程师/测试/reviewer 完成全链路"}
      ],
      "multiSelect": false
    },
    {
      "question": "是否需要 OpenClaw 后台执行？",
      "header": "OpenClaw",
      "options": [
        {"label": "不需要", "description": "只保留本地协作链路（推荐默认）"},
        {"label": "需要", "description": "生成远程控制/后台执行脚本，任务可后台继续跑"}
      ],
      "multiSelect": false
    }
  ]
}
```

If the user already provided some answers in their initial message, skip those questions and only ask for what's missing.

### Step 2 — Convert answers to parameters

| 用户选择 | 参数 |
|----------|------|
| 有设计稿 | `--path-mode design-driven` |
| 没有设计稿 | `--path-mode zero-to-one` |
| 多模型协作 | `--workflow claude-planner-codex-builder` |
| 单模型多角色 | `--workflow codex-fullstack-workflow` |
| 需要 OpenClaw | `--openclaw` |

### Step 3 — Run scaffold script

```bash
python3 scripts/init_designer_vibecoding_project.py \
  --target "<target-dir>" \
  --project-name "<project-name>" \
  --path-mode zero-to-one|design-driven \
  --workflow claude-planner-codex-builder|codex-fullstack-workflow \
  [--openclaw]
```

If target directory is non-empty, ask the user to confirm merge before adding `--merge`.

### Step 4 — Post-scaffold summary

Show the user:
- Which path was chosen and which workflow is active
- First 3 files to open: `AGENTS.md` → `agent-context/current-workflow.md` → `project-management/active-sprint.md`
- Which placeholders still need to be filled (`tasks/todo.md`, `.agent/handoff.json`)
- Available npm scripts (and OpenClaw scripts if enabled)

## Guidance

- `design-driven` only when the user already has a design source
- `codex-fullstack-workflow` when the user wants one environment to own the whole loop
- `claude-planner-codex-builder` when the user explicitly wants Claude to manage planning/context
- `OpenClaw` only when the user actually wants background/remote execution
- `agent_run.sh` is a placeholder — remind the user to configure `CONFIGURED=true` and fill `run_task()` before running

## Resources

- `references/template-map.md`: question wording, structured form mapping, path/mode behavior details
- `scripts/init_designer_vibecoding_project.py`: scaffold implementation
