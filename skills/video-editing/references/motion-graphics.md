# Motion graphics: minimal, animated, intentional

Modeled on short-form tech Reels the user picked as references: floating
screenshot cards, light backdrops, small accent words in an italic serif, smooth
blur-in motion, and one soft sound per visual change.

## Look

- **No black backgrounds or black fills.** Cards are light frosted glass:
  `rgba(255,255,255,.95)`, radius 30-44 px, shadow
  `0 18px 48px rgba(18,28,56,.14), 0 2px 6px rgba(18,28,56,.06)`, inset 1.5 px
  white rim. Icons sit in tinted circles (accent at 10-12% opacity), never in
  solid dark boxes. Phone mockups use a thin white frame, no black bezel.
- **Tokens:** ink `#16181D`, muted `#7C828E`, accent blue `#2F6BFF`,
  green `#1EAD57`, red `#F2463C`, tint `rgba(47,107,255,.10)`.
- **Type:** TikTok Sans 500-700 for body, Instrument Serif Italic for the one
  key word or phrase per graphic (in the accent color, ~1.3x size), e.g.
  "Good decision making, *made visible.*" Step numbers are serif italic ("01").
- Full-screen cutaways use a light radial gradient
  (`#FFFFFF -> #F1F3F8 -> #E6EAF1`) that slowly scales (8 s, 1.00 -> 1.06).

## Placement

Graphics never cover the face: put them in the bottom third. Measure each
rendered overlay's visible content (union of alpha > 12 over its frames), then
fit it into the band from max(0.667, face bottom + 0.015) to 0.935 of frame
height (face boxes from Apple Vision on the clips under the graphic). Scale down
when the content is taller than the band; sit it slightly above the band's
centre. If that would shrink it below legibility (e.g. a repo screenshot at
<60%), make it a full-screen cutaway on a light backdrop instead. Only
full-screen cutaways may cover the speaker.

## Motion

| Moment | Animation |
|---|---|
| Enter | 0.45 s, `cubic-bezier(.16,1,.3,1)`: opacity 0 -> 1, blur 16 px -> 0, translateY 24 px -> 0, scale .965 -> 1 |
| Hold | slow push-in, scale 1.00 -> 1.03 over the graphic's duration |
| Exit | 0.28 s: blur to 12 px, fade, rise 12 px |
| Text | word-by-word blur reveal, 70 ms stagger |
| Lists | items rise in on the word that names them; checks draw on (stroke-dashoffset) |
| Emphasis | underline or highlight grows left -> right after the accent word lands |
| Numbers | counters roll up (ease-out cubic) |
| Proof screenshots | a soft accent scan line sweeps before the verdict badge appears |
| CTA | link text with an underline that draws, arrow nudging every ~1.2 s |

Anchor every graphic's start to the word that introduces it and its end to the
end of the idea (or the next graphic's start). Minimum ~1.2 s on screen; give
reading-heavy graphics (file trees, screenshots) 2 s+.

## Sound design

- One soft entry swoosh (~0.16 volume) for most graphics.
- One accent per graphic at most, on the moment that matters: ding when proof
  lands ("0 secrets found", a checklist completes), click when a CTA link
  draws, notification on "comment ___", bell on a celebration card, soft
  ticks for list items after the first, sparse key clicks for typing.
- Library: when the Ocular Sounds packs are available (Jensy's Angel drive:
  `/Volumes/Angel/Ocular Sounds/Unzipped`), use them instead of stock UI sounds:
  Momentum `Whooshes - Short/Swing` for graphic entries, Momentum
  `Whooshes - Medium/Air Spirit` for full-screen cutaways (start 0.15 s before
  the cut so the peak lands on it), single clicks only for ticks, CTAs and list
  items (Vector `UIClick_CLICK-Keyboard Click 01`, `MECHClik ... Controller Button
  Click 02` — one transient each; Mechanica gears are ratchets, not single clicks),
  no keystroke sequences for typing (one click on "send"), Felt pure piano ping for proof/"done" moments, Felt major chord
  for celebrations. Most Momentum whooshes are heavy cinematic low end; prefer
  the airy ones (high centroid) and high-pass at 110-140 Hz.
- Level: trim each sound so the hit is near its start, peak-normalize to
  -3 dBFS, then set every SFX clip to -10 dB in the editor (0.316 linear).
  -7.5 dB was still too loud.
  SFX should sit under the voice, never compete with it.
- Never stack a pop on every list item; never more than two sounds per graphic.

## Rendering pipeline

- Author each graphic as HTML/CSS with Web Animations, then render
  frame-accurately with Playwright: for each frame, pause every animation and
  set `currentTime = t` (and call a `window.tick(t)` hook for scripted parts such
  as typing, counters, or screen recordings). Screenshot with
  `omitBackground: true` for transparency.
- Encode: transparent -> ProRes 4444 intermediate (`prores_ks -profile:v 4
  -alpha_bits 8`) -> **VideoToolbox HEVC-with-alpha for CapCut**
  (`scripts/to_hevc_alpha.sh`); opaque cutaways -> H.264 CRF 15.
- QA with contact sheets: extract the overlay frame to PNG first, then
  composite it over the real talking frame at its placement (two-input ffmpeg
  seeking misaligns timing).

## Reference study

1. `yt-dlp -o "%(id)s.%(ext)s" <url>` for each reference (public Reels work
   anonymously).
2. Contact sheet at 2 fps with timestamps:
   `ffmpeg -i ref.mp4 -vf "fps=2,scale=180:-2,drawtext=text='%{pts\:hms}':x=3:y=3:fontsize=13:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=10x5" sheet_%d.jpg`
3. Note layout (split screen vs floating card), entrance/exit motion, type
   pairing, accent usage, and where sounds land relative to visual changes.
