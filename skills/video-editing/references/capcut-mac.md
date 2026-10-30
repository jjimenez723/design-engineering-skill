# Building CapCut drafts on macOS

Verified on CapCut 8.9.x for Mac (App Store build, bundle `com.lemon.lvoverseas`).
Generate the draft JSON directly; do not build timelines by clicking through the UI.

## Where things live

| What | Path |
|---|---|
| Drafts | `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/<name>/` |
| Draft registry | `.../com.lveditor.draft/root_meta_info.json` (`all_draft_store`) |
| Media the draft points at | `~/Movies/CapCut Media/<project>/{media,overlays,sfx}` |
| Custom fonts | `~/Library/Containers/com.lemon.lvoverseas/Data/Movies/CapCut/User Data/Cache/effect/9900000NN/<font>/<file>.ttf` |

## Sandbox rule (the "Link media / File not accessible" error)

The App Store build can read only `~/Movies`, its own container,
`/Applications/CapCut.app`, and files the user picked in its import dialog.
Anything in `~/Downloads`, external drives, or project folders shows as
"File not accessible". So:

- Copy every referenced file under `~/Movies/CapCut Media/<project>/` and strip
  `com.apple.quarantine` on the copies.
- Make the builder **refuse to save** when any video/audio/font path is outside
  `~/Movies/`, the container, or the app bundle, or does not exist.

## Draft files

Per draft folder:

- `draft_info.json` and an identical copy at `Timelines/<timeline_id>/draft_info.json`
- `Timelines/project.json` (`main_timeline_id`, timeline list)
- `timeline_layout.json`, `draft_meta_info.json` (`draft_id`, `draft_name`,
  `draft_fold_path`, `tm_duration` in microseconds), `draft_settings`,
  `draft_virtual_store.json`, plus agency/biz/performance config copied from a template
- Register the draft in `root_meta_info.json` (insert at index 0; clear cloud fields).

Easiest reliable method: copy one draft that CapCut itself saved as a template,
extract one sample of each segment/material kind (main video, image overlay,
audio, text) and deep-copy those samples with new UUIDs, paths, and timeranges.

## Conventions inside `draft_info.json`

- Times are microseconds. Segment `source_timerange` = in-point in the media,
  `target_timerange` = position on the timeline.
- `clip.transform` is centered and normalized: x, y in [-1, 1], with
  `y = 1 - 2 * y_from_top` (0.7 from the top -> y = -0.4).
- `clip.scale = 1.0` fits the material's width to the canvas, so a 1080-wide
  overlay at scale 1.0 is pixel-exact on a 1080x1920 canvas (864-wide renders
  upscale to the same size).
- Bottom-band placement with scale s for an overlay W x H whose visible content
  is rows y0..y1: f = 1080 / W; content height = (y1 - y0) * f * s; asset centre
  = content centre - ((y0 + y1) / 2 - H / 2) * f * s; `transform.y = 1 - 2 *
  asset_centre / 1920`.
- Track layering: talking video `render_index` 0; full-screen cutaways
  11000; overlays 12000; text 14000. Put each SFX on an audio track, opening a
  new track only when sounds overlap.
- Text: put the font path in both `content.styles[].font.path` and
  `font_path`; size around 8-8.5 for 1080x1920 one-line captions; shadow
  `alpha 0.55`, `smoothing 0.18`, `distance 4`, angle -90.

## Media formats CapCut renders correctly

| Need | Use | Avoid |
|---|---|---|
| Transparent overlay | HEVC with alpha via VideoToolbox: `ffmpeg -i in.mov -an -c:v hevc_videotoolbox -alpha_quality 0.95 -pix_fmt bgra -b:v 12M -tag:v hvc1 out.mov` (QuickTime Animation `qtrle` also works but files are huge) | ProRes 4444 from `prores_ks` or `prores_videotoolbox`, avconvert `PresetHEVCHighestQualityWithAlpha` — all show a black box |
| Full-screen cutaway | H.264/HEVC mp4, opaque | — |
| iPhone HDR source | `avconvert -s in.mov -p PresetHighestQuality -o tmp.mov`, then encode tagged `bt709` | importing HLG directly (washed out) |
| Cut-out person/product | `scripts/mac_remove_bg_video.sh` / `mac_remove_bg.swift` (Apple Vision) | CapCut chroma key / remove-BG via desktop automation |

To test a new format quickly: build a scratch draft with one variant per
2-second slot over a talking clip, open it, and scrub each slot.

## Rebuild hygiene

- Quit CapCut first (`osascript -e 'quit app "CapCut"'`); it overwrites drafts
  and `root_meta_info.json` that it has open.
- CapCut renames drafts it picks up to `<name>(1)`. On rebuild, move `<name>` and
  every `<name>(N)` folder to the Trash and drop their registry entries, then
  write the new draft.
- Keep the previous overlay set as a backup folder before replacing assets.

## Verifying the result

- Open the draft (background app control is fine) and check the overlay track
  thumbnails and at least one overlay in the preview. If the user's screen is in
  a full-screen Space, background clicks are refused; say what was not checked.
- Confirm all 7 (or N) drafts appear on the CapCut home screen with the expected
  durations.
