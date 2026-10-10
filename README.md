# Design Engineering Skills for Claude and Codex

A small collection of cross-agent skills for polished product design and source-grounded video editing. The shared `SKILL.md` files use portable `name` and `description` frontmatter supported by both Claude Code and Codex. Codex-specific UI metadata is optional and can live in an `agents/openai.yaml` file.

## Included skills

- `emil-design-eng`: UI hierarchy, scanning, grouping, alignment, contrast, accessibility, forms, and interaction polish.
- `video-editing`: Purposeful cuts, beat-matched motion graphics, source-accurate captions, safe-area composition, and verified exports.

## Install for Codex

```bash
git clone https://github.com/jjimenez723/design-engineering-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R design-engineering-skill/skills/emil-design-eng design-engineering-skill/skills/video-editing "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex or begin a new task after installation.

## Install for Claude Code

```bash
git clone https://github.com/jjimenez723/design-engineering-skill.git
mkdir -p "$HOME/.claude/skills"
cp -R design-engineering-skill/skills/emil-design-eng design-engineering-skill/skills/video-editing "$HOME/.claude/skills/"
```

Restart Claude Code after installation. Invoke `$emil-design-eng` or `$video-editing` explicitly, or let the agent select a relevant skill automatically.

## Video editing quality standard

The video skill is based on a finished local edit workflow that required:

- timing grounded in verified audio rather than invented copy;
- cuts and graphics aligned to the spoken hook, proof, process, and CTA beats;
- safe-area placement that preserves faces, hands, microphones, and gestures;
- restrained, consistent cards and captions that remain readable at delivery size;
- visual frame inspection at key beats;
- metadata inspection and a full decode pass before delivery; and
- a concise report documenting the source cut, visual decisions, verification, and limitations.

## Layout

```text
skills/
├── emil-design-eng/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       └── ui-ux-foundations.md
└── video-editing/
    └── SKILL.md
```

## Attribution

The core `emil-design-eng` skill is adapted from [emilkowalski/skills](https://github.com/emilkowalski/skills), revision `d23d7f88a2e21c9e4b1418c7abe420f5c1052ba7`, under the MIT License. The UI/UX foundations reference and cross-agent packaging are local additions. The `video-editing` skill is a local workflow guide focused on source-grounded edits and export verification.
