#!/usr/bin/env python3
"""Aggressive de-silencing for talking-head takes. Prints JSON keep ranges (source seconds) + re-timed words.

usage: cut_silences.py clean.mov [--words whisper.json] [--keep-from WORD#N] [--keep-to WORD#N]

Default is AGGRESSIVE (short-form): pauses with breaths/room tone are cut too, not just true silence.
1. Adaptive threshold per clip: floor = 10th pct RMS, speech = 80th pct; thr = floor + 0.45*(speech-floor),
   clamped to [-40, -24] dB. silencedetect d=0.12. Then merge in RMS pauses (20 ms windows below the clip's
   speech median - 24 dB for >= 0.2 s) — breaths and room tone that silencedetect misses.
2. Cut every silence >= 0.14 s, keeping 0.05 s after the last word and 0.04 s before the next.
3. With whisper word timings (whisper-cli -ml 1 -sow -ojf, or [{"t0","t1","w"}]):
   a. REALIGN words into speech islands (non-silent spans >= 0.08 s). Whisper smears words across silence,
      worst at a take's head (one take had 6 of 10 words timed inside 3.5 s of silence -> captions out of sync
      and dead air kept). Off-island words are snapped forward into the next island, keeping order; islands that
      received them are re-timed by character weight; clean islands keep whisper's times clamped.
   b. Cut any remaining word gap > 0.22 s (keep 0.08 s tail / 0.05 s lead).
   c. Trim the take's head/tail to first word - 0.06 s / last word + 0.12 s (room noise often hides end silence).
4. Drop keep ranges shorter than 0.12 s.
Check afterwards: every transcript word must still be on the timeline (compare counts/text before vs after).
"""
import json, re, subprocess, sys

def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

def duration(src):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())

def silences(src):
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", src, "-af", "asetnsamples=n=800,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level", "-f", "null", "-"], capture_output=True, text=True)
    lv = sorted(float(x) for x in re.findall(r"RMS_level=(-?[\d.]+)", r.stderr))
    floor = lv[int(len(lv) * .10)] if lv else -60; speech = lv[int(len(lv) * .80)] if lv else -20
    thr = max(min(floor + 0.45 * (speech - floor), -24), -40)
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", src, "-af", f"silencedetect=n={thr:.1f}dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True)
    out, cur = [], None
    for l in r.stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", l)
        if m: cur = float(m.group(1))
        m = re.search(r"silence_end: ([\d.]+)", l)
        if m and cur is not None: out.append((cur, float(m.group(1)))); cur = None
    if cur is not None: out.append((cur, 9e9))
    return out, thr

def rms_pauses(src, rel_db=24, min_len=0.2):
    """Pauses the silence detector misses (breaths, room tone): 20 ms RMS below the clip's speech median - rel_db
    for >= min_len. Merged into the silence map so cuts, word realignment and captions all agree."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", src, "-af", "asetnsamples=n=960,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level", "-f", "null", "-"], capture_output=True, text=True)
    lv = [float(x) if x != "-inf" else -120.0 for x in re.findall(r"RMS_level=(-?[\d.]+|-inf)", r.stderr)]
    if not lv: return []
    hi = sorted(lv)[len(lv) // 2:]; thr = hi[len(hi) // 2] - rel_db; out, run = [], None
    for i in range(len(lv) + 1):
        q = i < len(lv) and lv[i] < thr
        if q and run is None: run = i
        if not q and run is not None:
            if (i - run) * 0.02 >= min_len: out.append((run * 0.02, i * 0.02))
            run = None
    return out

def merge(a, b):
    out = []
    for x, y in sorted(a + b):
        if out and x <= out[-1][1]: out[-1] = (out[-1][0], max(out[-1][1], y))
        else: out.append((x, y))
    return out

def load_words(p):
    j = json.load(open(p))
    if isinstance(j, dict) and "transcription" in j:  # whisper-cli -ojf
        return [[s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, s["text"].strip()] for s in j["transcription"]
                if s["text"].strip() and not s["text"].strip().startswith("[")]
    return [[w["t0"], w["t1"], w["w"]] for w in j]

def realign(fw, sil, D):
    isl, cur = [], 0.0
    for a, z in sil:
        if a > cur: isl.append((cur, min(a, D)))
        cur = max(cur, z)
    if cur < D: isl.append((cur, D))
    isl = [x for x in isl if x[1] - x[0] >= 0.08] or [(0.0, D)]
    ov = lambda a, z, x: max(0.0, min(z, x[1]) - max(a, x[0]))
    assign, prev = [], 0
    for w0, w1, w in fw:
        best = max(range(len(isl)), key=lambda i: ov(w0, w1, isl[i]))
        if ov(w0, w1, isl[best]) <= 0: best = next((i for i, x in enumerate(isl) if x[0] >= w1 - 0.02), len(isl) - 1)
        best = max(best, prev); prev = best
        assign.append((best, ov(w0, w1, isl[best]) < 0.5 * max(w1 - w0, 1e-3)))
    out = [None] * len(fw)
    for i in set(a for a, _ in assign):
        idx = [k for k, (a, _) in enumerate(assign) if a == i]; a0, a1 = isl[i]
        if any(assign[k][1] for k in idx):
            wt = [len(fw[k][2]) + 2 for k in idx]; tot = sum(wt); t = a0
            for k, q in zip(idx, wt):
                d = (a1 - a0) * q / tot; out[k] = [t, t + d, fw[k][2]]; t += d
        else:
            for k in idx:
                w0, w1, w = fw[k]; s = min(max(w0, a0), a1 - 0.04); out[k] = [s, max(s + 0.04, min(w1, a1)), w]
    return out

def find(ws, key):
    w, n = (key.split("#") + ["1"])[:2]; k = 0
    for i, x in enumerate(ws):
        if x[2].lower().strip(",.?!") == w.lower().strip(",.?!"):
            k += 1
            if k == int(n): return i
    sys.exit(f"anchor {key} not found")

def main():
    src = sys.argv[1]; D = duration(src); sil, thr = silences(src); sil = merge(sil, rms_pauses(src))
    ws = load_words(arg("--words")) if arg("--words") else []
    fw = realign(ws, sil, D) if ws else []
    s0, s1 = 0.0, D
    if sil and sil[0][0] < 0.15: s0 = max(0, sil[0][1] - 0.04)
    if sil and sil[-1][1] >= D - 0.05: s1 = min(D, sil[-1][0] + 0.10)
    kf, kt = arg("--keep-from"), arg("--keep-to")
    if kf: s0 = max(s0, fw[find(fw, kf)][0] - 0.10)
    if kt: s1 = min(s1, fw[find(fw, kt)][1] + 0.14)
    ranges, cur = [], s0
    for a, z in sil:
        if z - a >= 0.14 and a > s0 + 0.05 and z < s1 - 0.05:
            ranges.append((cur, a + 0.05)); cur = z - 0.04
    ranges.append((cur, s1))
    if fw:
        for ca, cz in [(x[1] + 0.08, y[0] - 0.05) for x, y in zip(fw, fw[1:]) if y[0] - x[1] > 0.22]:
            nr = []
            for a, z in ranges:
                if cz <= a or ca >= z: nr.append((a, z)); continue
                if ca > a: nr.append((a, ca))
                if cz < z: nr.append((cz, z))
            ranges = nr
        lo = -1 if kf else fw[0][0] - 0.06; hi = 9e9 if kt else fw[-1][1] + 0.12
        ranges = [(max(a, lo), min(z, hi)) for a, z in ranges if min(z, hi) > max(a, lo)]
    ranges = [(round(a, 3), round(z, 3)) for a, z in ranges if z - a > 0.12]
    kept = sum(z - a for a, z in ranges)
    inside = sum(1 for a, z, _ in fw if any(x - 0.02 <= a and z <= y + 0.02 for x, y in ranges))
    print(json.dumps({"source": src, "duration": round(D, 3), "kept": round(kept, 3), "threshold_db": round(thr, 1),
                      "words": len(fw), "words_inside_kept": inside, "ranges": ranges,
                      "words_realigned": [[round(a, 3), round(z, 3), w] for a, z, w in fw]}, indent=1))

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    main()
