# UI/UX Foundations

Use these rules when building or reviewing product UI. They are structural defaults, not a visual theme. Preserve a product's existing design language unless the user asks to change it.

## 1. Make scanning effortless

- Establish one obvious reading order. A user should identify the page purpose, current state, important values, and primary action in a quick scan.
- For compact label/value groups, place labels above their values and align related values on a shared axis. This is easier to scan than repeated left/right label-value pairs.
- Communicate status explicitly. Pair color with text, icon, shape, or position so status remains understandable without color.
- Show progress or completion when it affects the next decision, such as `2/3 complete`; do not make users infer it from scattered items.
- Use contrast to express hierarchy, not decoration. Primary content and actions need strong contrast; secondary content may recede but must remain legible.

## 2. Group with space before surfaces

- Start with a content layout: use proximity, spacing, alignment, and repeated rhythm to form groups.
- Do not wrap every logical group in a card, border, tinted box, or shadow. Excess containers flatten hierarchy and make every region compete equally.
- Add a surface only when it communicates something useful: emphasis, interaction, selection, ownership, elevation, or a distinct task boundary.
- Prefer fewer, larger structural surfaces over many nested cards. Sibling content usually belongs on one shared plane.
- Keep spacing within a group tighter than spacing between groups. If a group is unclear without a border, fix proximity and alignment first.

## 3. Minimize alignment anchors

- Default multi-line content, explanatory copy, prices, legal text, and stacked controls to left alignment. One consistent left edge reduces eye movement.
- Reserve centered text for short, self-contained moments such as a compact headline, empty state, or single call to action.
- Avoid stacking several centered lines with different widths. Each line creates a new visual anchor and makes comparison slower.
- Use proximity to bind supporting copy to the thing it explains. Remove distant or duplicated text rather than relying on decorative separators.

## 4. Make forms preserve context

- A field's label must remain identifiable while the field is focused and after it contains a value. Use a persistent label or a well-implemented floating label; placeholder-only fields lose context on entry.
- Use direct noun labels such as `Account number`, not instructional placeholders such as `Enter account number`.
- Give touch-first fields generous height. Use roughly 56 px for primary mobile form controls unless the product's platform conventions call for a different accessible size.
- Match the keyboard and input mode to the data. Show a numeric keypad for numeric identifiers and format structured values as the user types, while preserving an accessible raw value.
- Use moderate rounded rectangles for dense forms. Avoid fully pill-shaped text fields unless the pill communicates a specific control type; extreme radii reduce usable interior space and can distort floating-label corners.
- Keep validation inline, specific, and timely. Explain how to recover; do not wait until submission to reveal every error.
- Use sensible defaults and dependencies to reduce work, but keep them visible and reversible. For example, country may suggest currency without silently locking it.
- Make the primary action obvious and describe the next step. Disable it only when the reason is clear, and preserve entered data after recoverable errors.

## 5. Use hierarchy to communicate, not merely decorate

- Build hierarchy from order, size, weight, contrast, spacing, and state cues working together.
- Give the primary action one unmistakable emphasis level. Do not let secondary actions, cards, and decorative accents compete with it.
- Treat empty, loading, success, warning, error, disabled, and partial-completion states as part of the component, not as late additions.
- Check light/dark themes, reduced motion, high contrast, keyboard focus, zoom, and long/localized text before calling the interface complete.

## Review Order

Review in this sequence because later polish cannot rescue earlier structural problems:

1. Task path and reading order
2. Grouping and hierarchy
3. Alignment and proximity
4. Status, progress, and interaction feedback
5. Contrast and accessibility
6. Form context, ergonomics, validation, and recovery
7. Motion and decorative polish
