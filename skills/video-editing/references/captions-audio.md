# Captions and audio

## Audio (`scripts/clean_audio.py`)

1. Measure each channel (`pan=mono|c0=c0,volumedetect`, then `c1`). Phone and lav
   recordings often have the voice on one side only (other side ~-90 dB);
   averaging would halve the level. Take the louder side when they differ by
   more than 10 dB, otherwise average.
2. `highpass=f=80`; light `afftdn=nf=-25` on talking clips only.
3. Two-pass `loudnorm` (measure, then apply with `linear=true`), target -17 LUFS
   mono for talk (measures about -14 LUFS once duplicated to stereo) and -25 for
   B-roll (about -22).
4. Output dual mono (`pan=stereo|c0=c0|c1=c0`), AAC 256k, video stream copied.
5. Clips with no audio report `-inf`; copy them with plain AAC instead of failing.

## Transcription

- whisper.cpp `whisper-cli -m ggml-small.en.bin -l en -ml 1 -sow -ojf` gives
  per-word offsets. Use small.en or better; base mangles names.
- Verify proper nouns, the hook, and the CTA against the audio; keep a per-clip
  fix list (regex -> verified wording) and apply it before chunking.
- Whisper word times are not trustworthy around silence. Always realign words
  into speech islands (`scripts/cut_silences.py`) before cutting or timing
  captions. If a re-run changes the text, keep the verified text and only take
  the new timing (difflib-map new times onto old tokens).

## Caption chunking

- 2-5 words per caption (aim for 3-5), one line, <= 26 characters.
- Split preferably at punctuation and before conjunctions; avoid ending on a
  function word ("the", "of", "to", "and").
- Never split inside names and fixed phrases: add penalties for pairs such as
  `clifton|ave`, `animal|hospital`, `oasis|purified`, `purified|water`,
  `ai|home`, `home|lab`, `comment|<keyword>`, `10|years`. A small dynamic
  program over each clause (cost = length deviation + split penalties) works.
- **Blank when not talking.** Each caption starts at its first word and ends at its
  last word + 0.12 s — never at "the next caption's start". A caption never spans a
  pause: split clauses at word gaps > 0.25 s and at detected pauses (silence map +
  20 ms RMS below the speech median - 20/24 dB for >= 0.2 s), and never merge short
  clauses across a pause. If a pause begins inside a caption, end it 0.05 s after
  the pause starts. Minimum 0.35 s on screen unless the next caption starts sooner.
- Merge captions that would flash for under 0.25 s only when there is no gap
  between them.
- Verify on the final timeline: map each clip's pauses onto the timeline and assert
  no caption is visible for > 0.25 s of any pause and no captions overlap
  (`scripts/captions.py` `check()`).
- Style: TikTok Sans Medium, white, soft drop shadow (alpha .55, blur .18,
  distance 4), no box. Position just above the speaker's head (median face top
  - 0.085 of frame height, clamped 0.12-0.27 from the top); move to 0.085 from the
  top during full-screen cutaways. Use Apple Vision face boxes to measure.
