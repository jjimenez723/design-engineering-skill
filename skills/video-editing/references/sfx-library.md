# SFX library (`assets/audio/`)

Local one-shot sound library. Pick from here before generating or downloading
SFX. Ocular files are 96 kHz / 24-bit stereo WAV; resample to the project rate
(48 kHz) on export. For CapCut, copy only the files used into
`~/Movies/CapCut Media/<project>/sfx/` first (sandbox rule).

Licensing: the Ocular Sounds packs are a licensed commercial library. They are
git-ignored on purpose; never commit or publish them to the public repo.
Source on Angel: `/Volumes/Angel/Ocular Sounds/Unzipped/`.

| Folder | Files | Contents | Use for |
|---|---|---|---|
| `foundation/` | 75 | Booms 5, Impacts 15, Risers 15, Whoosh Hits 15, Whooshes 25 | cinematic hits, scene changes, build-ups into a reveal |
| `momentum/` | 100 | Impact 6, Movement 4, Sweeteners 17, Whooshes Long 15 / Medium 27 / Short 31 | transitions, text/card entrances, swipes, accents layered on cuts |
| `mechanica/` | 34 | Small Gears singular one-shots (01-34) | mechanical ticks, dials, counters, timeline/step reveals |
| `jensys-effects/` | 12 | Apple Pay, mouse click, mouse scroll, typing, push, iPhone message, voicemail, shutter (x2), vintage flash, beep, winding | UI/screen-recording moments, phone/notification beats, photo reveals |

## Picking rules

- Policy in `SKILL.md` still applies: one soft entry plus one accent on the
  moment that matters. The library is for choosing the right sound, not more.
- Short whoosh (`momentum/Whooshes - Short`) for card/text entrances; medium or
  long for full-screen transitions; riser (`foundation/Risers`) only into a
  real payoff; boom/impact on the single biggest beat.
- Trim to the transient, fade tails 50-150 ms, and sit SFX about 12-18 dB under
  the voice.
- List files with `find assets/audio -name '*.wav' -o -name '*.mp3'`; names
  describe the sound (e.g. `DSGNWhsh_WHOOSH SHORT-Blades_Ocular_Momentum.wav`).
