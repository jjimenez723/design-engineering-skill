# Design Engineering Skill for Claude and Codex

A cross-agent version of Emil Kowalski's `emil-design-eng` skill, extended with practical UI/UX rules for information hierarchy, scanning, grouping, alignment, contrast, accessibility, and forms.

The shared `SKILL.md` uses the portable `name` and `description` frontmatter supported by both Claude Code and Codex. Codex-specific UI metadata lives in `agents/openai.yaml`; Claude can ignore that optional directory.

## Install for Codex

```bash
git clone https://github.com/jjimenez723/design-engineering-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R design-engineering-skill/skills/emil-design-eng "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex or begin a new task after installation.

## Install for Claude Code

```bash
git clone https://github.com/jjimenez723/design-engineering-skill.git
mkdir -p "$HOME/.claude/skills"
cp -R design-engineering-skill/skills/emil-design-eng "$HOME/.claude/skills/"
```

Restart Claude Code after installation. Invoke it explicitly with `$emil-design-eng`, or let the agent select it for relevant UI work.

## What this version adds

- A more discriminating cross-agent description.
- No forced promotional greeting before answering the user's task.
- A progressive-disclosure UI/UX reference covering:
  - scanning and information hierarchy;
  - whitespace-first grouping and restrained surface use;
  - left alignment for dense and multi-line content;
  - status, progress, and contrast cues;
  - persistent form labels, touch-target sizing, input modes, formatting, validation, and recovery;
  - a practical UI review order that puts structure before decorative polish.
- Codex-native interface metadata without adding Claude-only frontmatter that Codex rejects.

## Layout

```text
skills/emil-design-eng/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── ui-ux-foundations.md
```

## Attribution

The core `emil-design-eng` skill is adapted from [emilkowalski/skills](https://github.com/emilkowalski/skills), revision `d23d7f88a2e21c9e4b1418c7abe420f5c1052ba7`, under the MIT License. The UI/UX foundations reference and cross-agent packaging are local additions.

