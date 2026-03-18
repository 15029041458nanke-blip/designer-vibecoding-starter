# Template Map

## Goal

Initialize a designer-friendly vibecoding project that can start working immediately with:

- `0-1` path: no design file, start from intent -> PRD -> implementation
- `design-driven` path: design input -> design analysis -> PRD -> implementation -> design QA
- `claude-planner-codex-builder`
- `codex-fullstack-workflow`
- optional `OpenClaw` background execution

## Questions to ask before scaffolding

Ask only these essentials:

1. Target directory or project name
2. Whether the project already has a design file
3. Which collaboration mode should be default:
   - `Multi-model collaboration`: use one model to manage planning / context and another model to execute implementation tasks
   - `Single-model multi-agent`: use one model to split into PM / architect / engineer / tester / reviewer roles and run the whole loop
4. Whether to include `OpenClaw` remote-control / background execution helpers

## Recommended wording

Use this exact wording when the host falls back to text questions:

1. `目标目录或项目名称是什么？`
   - `可以给我项目名，例如：my-app`
   - `也可以直接给我完整目录，例如：/Users/you/Desktop/my-project`
   - `如果你想直接在当前目录初始化，也请明确说明`

2. `项目是否已有设计稿？`
   - `有：会走 design-driven 路径，自动生成设计分析、设计约束、设计 QA 等文件`
   - `没有：会走 zero-to-one 路径，从意图澄清 -> PRD -> 实现开始`

3. `默认协作模式选哪个？`
   - `多模型协作：一个模型负责规划 / 上下文管理，另一个模型负责执行开发任务`
   - `单模型多子 agent：由一个模型拆成 PM / architect / engineer / tester / reviewer 等角色来完成整条链路`
   - `如果你已经明确要用 Claude + Codex，可以把它归到“多模型协作”这一项`
   - `如果你想由单一模型完成全流程，可以选“单模型多子 agent”`

4. `是否需要包含 OpenClaw？`
   - `需要：会生成远程控制 / 后台执行脚本，方便你不盯着本地窗口时继续跑任务`
   - `不需要：跳过 OpenClaw 相关脚本，只保留本地协作链路`

## Structured form mapping

If the host supports structured dialogs, map the questions like this:

- `project_name_or_target`
  - type: text
  - label: `项目名称或目标目录`
- `has_design`
  - type: single-select
  - options: `有设计稿`, `没有设计稿`
- `collaboration_mode`
  - type: single-select
  - options: `多模型协作`, `单模型多子 agent`
- `openclaw`
  - type: single-select
  - options: `需要 OpenClaw`, `不需要 OpenClaw`

Optional follow-up only when relevant:

- If design-driven: ask for a Figma/design source URL or a placeholder description
- If target directory already exists: confirm merge vs create nested folder

## Generated structure

The scaffold should create:

- `AGENTS.md`
- `agent-context/`
- `ai-workflows/`
- `docs/project-entry/`
- `docs/workflows/`
- `docs/design/`
- `docs/product/`
- `project-management/`
- `tasks/`
- `scripts/`
- `.agent/`
- optional `package.json` with workflow helper scripts

## Path-specific behavior

### zero-to-one

Create:

- product planning docs
- PRD/spec/todo templates
- no design-analysis requirement in default workflow text

Still include `docs/design/` as optional placeholders, but mark them as inactive.

### design-driven

Create:

- `docs/design/figma-source.md`
- `docs/design/design-analysis.md`
- `docs/design/design-contract.md`
- `docs/design/design-qa.md`

Make default workflow explicitly include design analysis and design QA.

## Mode-specific behavior

### claude-planner-codex-builder

Set:

- `agent-context/current-workflow.md` -> `claude-planner-codex-builder`
- workflow docs should say Claude handles planning/context, Codex handles execution

### codex-fullstack-workflow

Set:

- `agent-context/current-workflow.md` -> `codex-fullstack-workflow`
- workflow docs should say Codex owns product/architect/engineer/test/review by default

### openclaw

When enabled:

- include `scripts/openclaw_worker.sh`
- include `scripts/openclaw_daemon.sh`
- include `npm` helper scripts in `package.json`
- mention Git-based background execution in docs

When disabled:

- do not create OpenClaw scripts
- still keep `.agent/handoff.json` and `.agent/status.json`
