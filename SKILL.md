---
name: designer-vibecoding-starter
description: Initialize a designer-friendly vibecoding project scaffold with workflow files, collaboration modes, handoff/status infrastructure, and optional OpenClaw helpers. Use when starting a new project from scratch and you want Codex to set up the folder structure, choose between `0-1` or `design-driven` delivery, and configure either a multi-model planning/execution workflow or a single-model multi-agent workflow as the default collaboration mode.
---

# Designer Vibecoding Starter

## Overview

Ask the minimum setup questions, scaffold the project, and leave the user with a working folder structure that already contains the collaboration rules, templates, and execution entry points.

Read `references/template-map.md` before scaffolding when you need the exact path/mode behavior.

## Workflow

1. Ask these questions with clear options and short explanations:
   - target directory or project name
   - whether the project already has a design file
   - whether default mode should be:
     - `Multi-model collaboration` (claude-planner-codex-builder): both chains share the same complete role team; Claude leads the planning-side roles (design-analyst / product-strategist / project-manager / architect / reviewer) and Codex leads the execution-side roles (engineer / tester)
     - `Single-model multi-agent` (codex-fullstack-workflow): the same complete role team, but Codex drives all roles end-to-end in one model loop
   - whether to include `OpenClaw` as a remote-control / background execution layer (additive layer on top of either mode)
2. Convert the answers into:
   - `path_mode`: `zero-to-one` or `design-driven`
   - `workflow`: `claude-planner-codex-builder` or `codex-fullstack-workflow`
   - `openclaw`: enabled or disabled
3. Run:

```bash
python3 scripts/init_designer_vibecoding_project.py \
  --target "<target-dir>" \
  --project-name "<project-name>" \
  --path-mode zero-to-one|design-driven \
  --workflow claude-planner-codex-builder|codex-fullstack-workflow \
  [--openclaw]
```

4. After scaffolding, show the user:
   - which path was chosen
   - which workflow is active
   - which files to open first
   - which placeholders still need to be filled
5. If `design-driven` path was chosen, remind the user of the required Figma MCP setup:
   - Open `docs/design/figma-mcp-setup.md` for the 5-step guide
   - Get a Figma Personal Access Token (Settings > Security > Personal access tokens, Read-only, File content scope)
   - Create `.mcp.json` in the project root and fill in `FIGMA_API_KEY`
   - Run `npm install --save-dev vite-plugin-svgr` in the frontend project
   - Update `vite.config.ts`: `import svgr from 'vite-plugin-svgr'` and add `svgr()` to plugins
   - The scaffold already generated `docs/design/figma-mcp-setup.md` with the complete guide
6. If the user wants local/background execution, point them to:
   - `npm run workflow:intent`
   - `npm run agent:run`
   - `npm run openclaw:worker`
   - `npm run openclaw:daemon`
7. If `OpenClaw` is enabled, remind the user of the required git setup before the worker can run:
   - `git init` + push to GitHub (the worker does `git pull` on each cycle and `git push` after execution)
   - install `jq` (required by the worker for handoff parsing)
   - configure Git credentials (SSH key or HTTPS Personal Access Token, non-interactive)
   - fill in `scripts/agent_run.sh` (set `CONFIGURED=true` and add the real execution command)
   - run a dry-run first: `OPENCLAW_DRY_RUN=true npm run openclaw:worker`
   - the scaffold will print a step-by-step git setup checklist after initialization completes

## Guidance

- Prefer asking the setup questions as structured choices when the host supports interactive forms or dialogs.
- When asking in plain text, use the wording in `references/template-map.md` instead of improvising.

- Prefer `design-driven` only when the user already has a design source. In design-driven mode, `design-analyst` must be the first role activated before any handoff is created.
- In `design-driven` mode, the scaffold automatically generates `agent-context/design-role-rules.md` (7-category restoration rule set) and `docs/design/figma-mcp-setup.md` (5-step Figma MCP + vite-plugin-svgr guide). Both files require user action before icon downloads will work.
- Icon restoration uses a two-layer strategy: (1) **preferred** — use `download_figma_images` MCP tool to download SVG directly from Figma into `src/assets/icons/`, then import with `vite-plugin-svgr`; (2) **fallback** — render `<IconPlaceholder name="..." />` when the node ID is not a top-level exportable node or the token is not configured.
- Prefer `codex-fullstack-workflow` when the user wants one environment to own the whole loop (Codex drives all roles: PM / architect / engineer / tester / reviewer).
- Prefer `claude-planner-codex-builder` when the user explicitly wants Claude to manage planning and context (Claude drives: design-analyst / product-strategist / project-manager / architect / reviewer; Codex drives: engineer / tester).
- Both modes use the same complete role team — the difference is which model drives which roles.
- Include `OpenClaw` only when the user actually wants background/remote execution AND is willing to set up a GitHub repo with git credentials. The worker requires `git`, `jq`, a configured remote, and a non-interactive push setup.
- If the target directory already contains files, scaffold into it only when the user clearly intends to merge; otherwise create a nested project folder.

## Generated Project Shape

The scaffold should leave the user with:

- `AGENTS.md`
- `agent-context/`
- `ai-workflows/`
- `docs/project-entry/`
- `docs/workflows/`
- `docs/product/`
- `docs/design/`
- `project-management/`
- `tasks/`
- `scripts/`
- `.agent/`
- `package.json`

## Resources

- `references/template-map.md`: exact behavior for paths, modes, and questions
- `scripts/init_designer_vibecoding_project.py`: create the scaffold
