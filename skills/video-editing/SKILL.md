---
name: video-editing
description: Edit footage into polished, source-grounded short-form videos with aggressive silence cuts, beat-matched minimal motion graphics, intentional SFX, 3-5 word captions, and verified exports or native CapCut drafts. Use for requested editing or graphics deliverables (including building CapCut timelines on a Mac); do not use for video-only analysis, standalone subtitle work, generative restyling, or clip-variant testing.
metadata:
  short-description: Produce polished, source-grounded video edits
---

# Video editing

Use this skill when the user wants a finished video or an editing change: cuts,
pacing, de-silencing, overlays, animated cards, captions, SFX, background
removal, a CapCut timeline, or export packaging. Use the project's existing
editing stack when one exists; Higgsedit is appropriate for native editable
compositions, a local ffmpeg workflow when that is already the working path, and
a generated CapCut draft when the user asks for the edit "in my CapCut timeline".

The standard is not merely a playable file. The result should be a coherent,
source-faithful edit whose visuals support the spoken idea, whose captions are
accurate and in sync, and whose output has been visually inspected and decoded.

## Boundaries

- Do not activate for analysis, summaries, critiques, or scene-by-scene review
  without a requested edit.
- For caption burning or caption restyling as the whole request, use the
  dedicated subtitles skill when it is available.
- For targeted object replacement or ordered clip variants, use the dedicated
  ad-multiplier workflow when it is available.
- Never invent dialogue, transcript phrases, brand names, repository names, stats,
  or visual proof. A recreated UI (e.g. a ChatGPT answer) must reproduce a real,
  verified result word for word; caption people as heard, not as hoped.
- Preserve the original media and create a distinct output for each revision.
  Destroy old projects only when the user says so (move to Trash, not `rm`).

## House style (defaults unless the user says otherwise)

- **Talk to the user briefly.** Short status lines, compressed action lists, no
  recap of steps. Show picks/plans as a scannable list, then build.
- **Picks:** identify talking takes vs B-roll per video, choose the best take of
  each line, and say which clip covers which beat before cutting.
- **Pacing:** aggressive. Remove silences, breaths, room-tone pauses, and dead air
  at the head/tail of every take (see *Aggressive silence removal*). Jump cuts
  inside one take alternate a 1.00x / 1.08x punch-in so they read as intentional.
- **Captions:** 3-5 words, one line, never more than ~26 characters, TikTok Sans
  Medium, white with a soft shadow (no box), placed just above the speaker's head;
  moved to the top during full-screen cutaways. **Captions are only on screen while
  the speaker is talking**: a caption never spans a pause, ends at its last word
  (+0.12 s), and the screen goes blank during pauses ("Hey, this is Jensy." + pause
  = no text until the next word). `scripts/captions.py` enforces and checks this. Never split names ("Clifton Ave
  Animal Hospital", "AI home lab"). Details: `references/captions-audio.md`.
- **Audio:** fill both channels from the live mic, two-pass loudnorm to
  -14 LUFS (talk) / -22 LUFS (B-roll), remove breaths and silences.
- **Graphics placement:** always in the bottom third, below the face — never over
  the face. Fit each overlay's visible content (alpha bounding box) into the band
  from max(0.667, face bottom + 0.015) to 0.935 of frame height, scaling down when
  it does not fit. Full-screen cutaways are the only exception.
- **Graphics:** minimal, animated, and intentional — light frosted cards, no
  black backgrounds or black fills, blur-in entrances, draw-on checks/underlines,
  slow push-in while held, one accent color, key words in an italic serif.
  Details and tokens: `references/motion-graphics.md`.
- **SFX:** understated, every clip at -10 dB, Ocular Sounds when available (Momentum
  whooshes; Vector single clicks). Clicks are always single clicks — one transient,
  no ratchets, no keystroke barrages. At most one soft entry sound plus one accent on the
  moment that matters (ding on proof, click on a CTA, notification on
  "comment ___", bell on a celebration). No pop per list item. Pick sounds
  from the local library in `assets/audio/` (index: `references/sfx-library.md`).
- **Color:** iPhone-level. HDR (HLG/Dolby Vision) clips must be tone-mapped to
  SDR BT.709 with Apple's converter before editing, or they look washed out.
- **Study references when given.** Download them (`yt-dlp`), build timestamped
  contact sheets (2 fps), and extract layout, motion, type, color, and SFX
  patterns before designing. Summarize the patterns in a few bullets.

## Quality bar

### Source and story

- Inspect footage, audio channels, dimensions, frame rate, color transfer
  (`ffprobe ... color_transfer` — `arib-std-b67` means HLG), and duration first.
- Treat verified audio and footage as ground truth. Transcription only speeds
  up timing; manually check names, technical terms, the hook, and the CTA.
- Organize around real story beats: hook, context/proof, process, result, CTA.

### Visual system

- Tie every overlay to the word that introduces it (anchor graphics to word
  timestamps, not guesses) and keep it up for the whole idea.
- Protect face, eyes, hands, mic, and gestures; check the full frame at each
  overlay, including the bottom edge (stacked badges get clipped).
- Balance multi-line kinetic text (`text-wrap: balance`) so no word is orphaned.

### Captions and claims

- Correct transcription errors against the audio. Keep caption text and
  overlay text consistent with the final audio.
- Whisper timing is unreliable around silence; realign words into speech
  islands before cutting or captioning (built into `scripts/cut_silences.py`).
- Every transcript word must survive the cut: compare word counts/text before
  and after de-silencing.

## Aggressive silence removal (default)

Run `scripts/clean_audio.py` first, then `scripts/cut_silences.py` with whisper
word timings (`whisper-cli -ml 1 -sow -ojf`). Defaults:

| Setting | Value |
|---|---|
| Threshold | per clip: floor(p10 RMS) + 0.45 x (speech(p80) - floor), clamped -40..-24 dB |
| Detection | `silencedetect d=0.12` |
| Cut | every silence >= 0.14 s; keep 0.05 s tail, 0.04 s lead |
| Word-gap cut | any realigned word gap > 0.22 s (breaths/room tone); keep 0.08 s tail, 0.05 s lead |
| Head/tail | trim to first word - 0.06 s / last word + 0.12 s |
| Min piece | drop keep ranges < 0.12 s |

Before trusting the cut, realign words: whisper smears early words across
leading silence (seen: 6 of 10 words inside 3.5 s of silence), which both keeps
dead air and puts captions out of sync. If whisper text changes on a re-run,
keep the previously verified text and only take the new timings.

## Background removal on macOS

Use Apple's native Vision background remover (same engine as Finder/Preview
"Remove Background"). Do **not** drive CapCut's chroma key or "Remove
background" with desktop automation — it is slow, unverifiable, and not
reproducible.

- Stills / logos / products: `swift scripts/mac_remove_bg.swift in.png out.png`
  (foreground-instance mask; `--mode person` for people).
- Video: `scripts/mac_remove_bg_video.sh in.mov out.mov person` — extracts
  frames, masks each with Vision (person segmentation is steadier frame to
  frame), and encodes HEVC-with-alpha that CapCut displays correctly.
- Inspect a composite over a solid color before placing it.

## CapCut on macOS (native drafts)

Building the timeline directly as a CapCut draft is preferred over UI
automation. Read `references/capcut-mac.md` before writing any draft. The
non-negotiables:

1. **Sandbox:** CapCut (App Store build) can read only `~/Movies`, its own
   container, and files picked in its dialog. Copy every clip, overlay, SFX, and
   font-referenced file under `~/Movies/CapCut Media/<project>/` or the draft
   opens with "Link media / File not accessible". The builder must refuse to save
   if any path is elsewhere.
2. **Alpha overlays:** CapCut draws a black box behind ProRes 4444 alpha and
   behind avconvert's HEVC-alpha preset. Use VideoToolbox HEVC with alpha:
   `scripts/to_hevc_alpha.sh` (`hevc_videotoolbox -alpha_quality 0.95 -pix_fmt
   bgra -tag:v hvc1`).
3. **HDR clips:** `avconvert -p PresetHighestQuality` first (Apple tone mapping),
   then encode tagged bt709.
4. **Quit CapCut** before writing drafts; register each draft in
   `root_meta_info.json`; replace `<name>` and CapCut's renamed `<name>(1)` copies
   (move to Trash) on rebuild.
5. **Fonts** go in CapCut's own effect cache so the sandbox can load them.

## Preferred workflow

1. **Inventory** clips, audio channels, HDR flags, target format, and existing
   timing data. Record the starting state.
2. **Clean audio** (`clean_audio.py`) and **transcribe** (whisper small.en or
   better, word level). Verify hook, names, CTA.
3. **Pick takes** and present the plan (talking vs B-roll per beat).
4. **Cut** with `cut_silences.py`; build the timeline (segments, words,
   captions) in a reviewable JSON manifest.
5. **Design graphics** from the beat map (reference study first if given);
   render with the frame-accurate renderer in `references/motion-graphics.md`;
   encode alpha overlays for the target editor.
6. **Assemble** — ffmpeg render, or CapCut draft per `references/capcut-mac.md`.
7. **Inspect**: contact sheets at the hook, every overlay (composite extracted
   PNG frames, not seeked two-input overlays), caption changes, and CTA; open
   the CapCut draft and scrub at least one overlay to confirm transparency.
8. **Verify files**: `ffprobe` + full decode to null. When files cross machines,
   compare decoded-frame MD5 (`ffmpeg -i f -map 0:v -f md5 -`); container bytes
   may legitimately differ.
9. **Hand off**: say what changed in one or two sentences, where it lives, and
   any limitation.

## Known failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| CapCut "Link media / File not accessible" | media outside the sandbox | copy under `~/Movies`, builder guard |
| Black box behind graphics in CapCut | ProRes 4444 / avconvert HEVC alpha ignored | `to_hevc_alpha.sh` (VideoToolbox HEVC alpha) |
| Washed-out iPhone footage | HLG not tone-mapped | `avconvert -p PresetHighestQuality`, tag bt709 |
| Duplicate "(1)" drafts | CapCut renames drafts it picks up | rebuild replaces `<name>` and `<name>(N)` |
| Quiet, one-sided voice | lav on one channel only | pick live channel, dual-mono out |
| Captions out of sync / dead air at take start | whisper smears words over silence | realign into speech islands |
| Words missing after cuts | words timed in cut silence | realign, then assert word count unchanged |
| Captions split names / flash / overlap | naive chunking | DP chunker with name penalties, merge < 0.25 s, clamp to next |
| Overlay misplaced in QA sheet | ffmpeg seek on two inputs | extract PNG frames first, then composite |
| Bottom badges clipped | overlay y too low | check full frame, raise y |
| Orphan word in kinetic text | default wrapping | `text-wrap: balance` |
| Caption still showing during a pause | caption end clamped to next caption start | end at last word + 0.12 s, split at pauses, `captions.py` check |
| Pauses survive the cut (breaths, room tone) | silencedetect misses non-silent pauses | merge RMS pauses (median - 24 dB, >= 0.2 s) into the silence map |
| Graphic covers the face | fixed mid-frame y | bottom-third band from alpha bbox + face boxes |
| SFX too loud / busy | stock levels, multi-click sounds | -10 dB, single-transient clicks only |

## Bundled files

| File | Use |
|---|---|
| `scripts/clean_audio.py` | live-channel pick, two-pass loudnorm, dual mono |
| `scripts/cut_silences.py` | aggressive de-silencing (silence map + RMS pauses) + word realignment -> JSON keep ranges |
| `scripts/captions.py` | 3-5 word captions that are blank during pauses, with a built-in check |
| `scripts/mac_remove_bg.swift` | Apple Vision background removal for images / frame folders |
| `scripts/mac_remove_bg_video.sh` | video cut-out -> HEVC-with-alpha |
| `scripts/to_hevc_alpha.sh` | convert alpha overlays to the format CapCut honors |
| `scripts/render_overlays.js` | frame-accurate HTML/CSS -> video renderer (Playwright) |
| `assets/overlay-base.css` | design tokens + enter/hold/exit/draw-on animations |
| `assets/audio/` | SFX library: `foundation/`, `momentum/`, `mechanica/` (Ocular singulars), `jensys-effects/` (local only, git-ignored) |
| `references/sfx-library.md` | what's in each SFX folder and when to use it |
| `references/capcut-mac.md` | draft format, sandbox, formats, rebuild hygiene |
| `references/motion-graphics.md` | look, motion, SFX policy, rendering, reference study |
| `references/captions-audio.md` | audio chain, transcription, caption chunking and placement |

## Completion checklist

- Distinct, playable output (file or CapCut draft) in the requested format.
- Audio filled on both channels, normalized, silences/breaths removed, every
  word still present.
- Captions 3-5 words, one line, in sync, names intact, matched to verified speech,
  and blank whenever nobody is talking (run the pause check on the final timeline).
- Graphics minimal, no black backgrounds, transparent in the target editor, in the
  bottom third below the face, fully inside the frame.
- SFX sparse and on the beat that matters.
- Key frames inspected at output size; metadata check and full decode pass.
- Limitations documented.
