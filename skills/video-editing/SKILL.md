---
name: video-editing
description: Edit footage into polished, source-grounded videos with purposeful cuts, motion graphics, captions, and verified exports. Use for requested editing or graphics deliverables; do not use for video-only analysis, standalone subtitle work, generative restyling, or clip-variant testing.
metadata:
  short-description: Produce polished, source-grounded video edits
---

# Video editing

Use this skill when the user wants a finished video or an editing change: cuts,
pacing, soundtrack-preserving trims, overlays, animated title cards, captions,
or export packaging. Use the project's existing editing stack when one exists;
Higgsedit is appropriate for native editable compositions, while a local
ffmpeg-based workflow is appropriate when that is already the working path.

The standard is not merely a playable file. The result should be a coherent,
source-faithful edit whose visuals support the spoken idea, whose captions are
accurate and readable, and whose final export has been both visually inspected
and technically decoded.

## Boundaries

- Do not activate for analysis, summaries, critiques, or scene-by-scene review
  without a requested edit.
- For caption burning or caption restyling as the whole request, use the
  dedicated subtitles skill when it is available.
- For targeted object replacement or ordered clip variants, use the dedicated
  ad-multiplier workflow when it is available.
- Do not invent dialogue, transcript phrases, brand names, repository names, or
  visual proof that is not supported by the supplied media or verified source.
- Preserve the original media and create a distinct output for each meaningful
  revision.

## Quality bar

### Source and story

- Inspect the available footage, audio, dimensions, frame rate, duration, and
  existing project structure before changing the timeline.
- Treat the verified audio and footage as ground truth. Use transcription to
  accelerate timing, then manually check names, technical terms, and the hook.
- Make every cut earn its place. Remove duplicate material, dead pauses, or
  distracting tail moments only when the change improves comprehension or
  momentum; preserve a gesture or reaction when it carries meaning.
- Organize the edit around the actual story beats: hook, context or proof,
  process, result, and call to action when those beats exist. Do not force a
  template onto footage that does not support it.

### Visual system

- Tie overlays, cards, titles, and transitions to the spoken idea they explain;
  they should clarify the hook, tool, action, proof, or CTA rather than decorate
  empty time.
- Keep a restrained, consistent visual language: a small type system, clear
  hierarchy, deliberate accent color, and transitions that do not compete with
  the speaker.
- Protect the face, eyes, hands, microphone, and meaningful gestures. Place
  cards in open safe areas and check the full frame at the moments where the
  subject moves, points, or changes position.
- Prefer readable overlays that remain on screen for the full idea they support.
  Avoid rapid flashes, stacked UI noise, or cards that obscure the proof.
- Preserve the intended aspect ratio and platform framing. Check crop, edge
  safety, contrast, and legibility at the actual delivery size.

### Captions and claims

- Correct obvious transcription errors against the audio, including product,
  brand, repository, and technical names.
- Keep caption timing aligned to speech and break lines for one-pass reading.
  Use styling that remains legible over motion without an opaque box unless the
  footage requires one.
- Never caption an unsupported phrase merely because it would improve the hook.
  Record the limitation in the edit report when requested wording is not
  present or clear in the audio.
- Keep captions and overlays semantically consistent with each other and with
  the final audio.

## Preferred workflow

1. **Inventory the source.** Identify the project, source clips, audio, target
   format, existing timing data, and any duplicate or reference-only media.
   Record the starting state so the source remains recoverable.
2. **Establish the spoken timeline.** Transcribe with the available local or
   project-supported tool. Verify the hook, proper nouns, technical terms, and
   CTA against the audio before building caption or overlay timing.
3. **Plan the cut.** Map shots and graphics to real story beats. Tighten dead
   space with a reason, keep important gestures intact, and preserve original
   audio unless the user explicitly asks for a soundtrack change.
4. **Build the visual treatment.** Create cards, titles, and motion graphics
   from the beat map. Keep the hierarchy consistent, use safe areas, and make
   each graphic support a specific idea.
5. **Render a distinct revision.** Keep source and prior renders intact. Export
   the requested codec, dimensions, frame rate, and audio in a durable output
   location. Produce an SRT or other sidecar when it is useful for the request.
6. **Inspect the result.** Sample frames or a contact sheet at the hook, every
   major graphic beat, transitions, caption changes, and CTA. Check for
   obstruction, clipping, unreadable type, bad crops, stale cards, and caption
   drift.
7. **Verify the file.** Run metadata inspection such as `ffprobe` and a full
   decode to a null sink or equivalent. A render that was interrupted, has a
   missing container index, or cannot decode is not complete; rerender it before
   reporting success.
8. **Package the handoff.** Deliver the final video and any sidecars, plus a
   concise report covering the source cut, visual decisions, verification, and
   known limitations. Link the actual files, not only an internal project path.

## Tool and project guidance

- For Higgsedit projects, prefer the native project and composition APIs so the
  edit remains inspectable and editable. Use bounded operations on an existing
  human/shared edit; a whole-script rebuild is appropriate only when replacing
  the intended timeline.
- For local ffmpeg or graphics workflows, reuse the existing project scripts,
  timing manifests, fonts, overlays, and render conventions before introducing
  a new pipeline.
- Keep timing data in a reviewable manifest or sidecar when the workflow uses
  one. Regenerate derived overlays and captions from the corrected source data
  instead of patching only a final composite.
- If a required input, credential, or source fact is missing, preserve the
  source and report the smallest concrete blocker rather than fabricating a
  result.

## Completion checklist

Before calling the edit finished, confirm:

- The output is a distinct, playable file in the requested format.
- The audio is preserved or intentionally changed, and the export has the
  expected duration and streams.
- The hook, proof/process beats, and CTA are visually legible where present.
- Captions match verified speech, including names and technical terms.
- Graphics do not cover faces, hands, microphones, or meaningful gestures.
- Key frames have been inspected at the actual output size.
- Metadata inspection and a full decode pass succeed.
- Any unsupported requested wording or other limitation is documented.
