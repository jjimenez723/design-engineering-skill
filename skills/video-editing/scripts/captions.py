#!/usr/bin/env python3
"""Short-form captions that are only on screen while someone is talking.

usage: captions.py words.json [--pauses pauses.json] [--keep "clifton ave" --keep "ai home lab"] > captions.json
  words.json  : [[t0, t1, "word"], ...] on the FINAL timeline (after cuts), realigned to speech
  pauses.json : [[a, b], ...] timeline intervals where the voice stops (silence map + RMS pauses, >= 0.2 s)

Rules (house style):
- 2-5 words, one line, <= 26 characters; split at punctuation, avoid ending on a function word; never split a
  --keep phrase (names, products) across captions.
- A caption NEVER spans a pause: a word gap > 0.25 s or a detected pause between two words starts a new caption,
  and short clauses are not merged across a pause.
- On-screen time = first word start -> last word end + 0.12 s hold, never past the next caption, cut back to
  0.05 s after any pause that begins inside it. Minimum 0.35 s unless the next caption starts sooner.
So after "Hey, this is Jensy." + pause, the screen is blank until the next word.
"""
import json, re, sys

PAUSE, HOLD, MIN_CAP, MAXCH = 0.25, 0.12, 0.35, 26
FUNC = set("the a an of to my your and but so that for with in on at is it are be".split())
CONJ = set("and but so then because which that when if".split())
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())

def build(words, pauses=(), keep=()):
    wtl = [{"t0": a, "t1": b, "w": w} for a, b, w in words]
    nosplit = {}
    for ph in keep:
        toks = [norm(t) for t in ph.split()]
        for x, y in zip(toks, toks[1:]): nosplit[(x, y)] = 9
    for w in wtl:  # a word ends where the voice stops
        for a, z in pauses:
            if w["t0"] + 0.06 <= a < w["t1"]: w["t1"] = a
    def is_pause(w, nx):
        return nx["t0"] - w["t1"] > PAUSE or any(w["t0"] < a and a + 0.1 < nx["t0"] + 0.06 and z > nx["t0"] - 0.1 for a, z in pauses)
    clauses, cur = [], []
    for k, w in enumerate(wtl):
        cur.append(w)
        if re.search(r"[.,?!;:…]$", w["w"]) or (k + 1 < len(wtl) and is_pause(w, wtl[k + 1])): clauses.append(cur); cur = []
    if cur: clauses.append(cur)
    L = lambda c: len(" ".join(x["w"] for x in c))
    def best(c):
        n = len(c); dp = [0] + [1e9] * n; bk = [0] * (n + 1)
        for j in range(1, n + 1):
            for i in range(max(0, j - 5), j):
                g = c[i:j]
                if L(g) > MAXCH and j - i > 1: continue
                k = j - i; cost = (k - 3.5) ** 2 + (6 if k == 1 and n > 1 else 0) + (1.5 if k == 2 and n > 2 else 0)
                if j < n:
                    last, nxt = norm(c[j - 1]["w"]), norm(c[j]["w"])
                    cost += (3 if last in FUNC else 0) - (1 if nxt in CONJ else 0) + nosplit.get((last, nxt), 0)
                if dp[i] + cost < dp[j]: dp[j] = dp[i] + cost; bk[j] = i
        out, j = [], n
        while j > 0: out.append(c[bk[j]:j]); j = bk[j]
        return out[::-1]
    groups = []
    for c in clauses:
        if groups and len(c) <= 2 and len(groups[-1]) + len(c) <= 5 and L(groups[-1] + c) <= MAXCH - 1 \
                and not re.search(r"[.?!…]$", groups[-1][-1]["w"]) and not is_pause(groups[-1][-1], c[0]):
            groups[-1] = groups[-1] + c
        else: groups += best(c)
    caps = []
    for i, c in enumerate(groups):
        t0 = c[0]["t0"]; nxt = groups[i + 1][0]["t0"] if i + 1 < len(groups) else 9e9
        t1 = min(nxt, c[-1]["t1"] + HOLD)
        if t1 - t0 < MIN_CAP: t1 = min(nxt, t0 + MIN_CAP)
        for a, z in pauses:
            if t0 + 0.1 < a < t1: t1 = min(t1, a + 0.05)
        caps.append({"text": " ".join(x["w"] for x in c).rstrip(",;:"), "t0": round(t0, 3), "t1": round(t1, 3)})
    return caps

def check(caps, pauses, limit=0.25):
    """Problems: any caption visible during > limit s of a pause, or overlapping the next caption."""
    bad = [c["text"] for c in caps for a, z in pauses if min(z, c["t1"]) - max(a, c["t0"]) > limit]
    bad += [f"overlap: {a['text']}" for a, b in zip(caps, caps[1:]) if a["t1"] > b["t0"] + 1e-6]
    return bad

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    args = sys.argv[1:]
    words = json.load(open(args[0]))
    pauses = json.load(open(args[args.index("--pauses") + 1])) if "--pauses" in args else []
    keep = [args[i + 1] for i, a in enumerate(args) if a == "--keep"]
    caps = build(words, pauses, keep)
    probs = check(caps, pauses)
    if probs: print("PROBLEMS:", probs, file=sys.stderr)
    print(json.dumps(caps, indent=1))
