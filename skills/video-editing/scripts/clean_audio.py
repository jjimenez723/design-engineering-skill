#!/usr/bin/env python3
"""Fill both channels + normalize a clip's audio (video stream copied untouched).

usage: clean_audio.py in.mov out.mov [--broll]

- Picks the live mic channel: lav/phone mics often record on ONE channel (other side ~-90 dB).
  Averaging would halve the level; we take the louder side when they differ by >10 dB.
- High-pass 80 Hz, light denoise on talking clips, two-pass linear loudnorm, then dual-mono out.
- Targets: talk -17 LUFS mono (measures ~-14 LUFS once duplicated to stereo), B-roll -25 (~-22).
- Clips with no audio (loudnorm reports -inf) are copied with plain AAC instead of failing.
"""
import json, re, subprocess, sys

def mean(src, pan):
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", src, "-map", "0:a:0", "-af", f"pan=mono|c0={pan},volumedetect", "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"mean_volume: (-?[\d.]+)", r.stderr)
    return float(m.group(1)) if m else -99.0

def main(src, out, talk=True):
    L, R = mean(src, "c0"), mean(src, "c1")
    ch = "c0" if L - R > 10 else ("c1" if R - L > 10 else "0.5*c0+0.5*c1")
    tgt = -17 if talk else -25
    pre = f"pan=mono|c0={ch},highpass=f=80" + (",afftdn=nf=-25" if talk else "")
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", src, "-map", "0:a:0", "-af", f"{pre},loudnorm=I={tgt}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    try:
        m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    except ValueError:
        m = {"input_i": "-inf"}
    if m["input_i"] in ("-inf", "inf"):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-map", "0:v:0", "-map", "0:a:0?", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", out], check=True)
        print(json.dumps({"channel": ch, "lufs": None, "note": "silent source"})); return
    ln = (f"loudnorm=I={tgt}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy",
                    "-af", f"{pre},{ln},aresample=48000,pan=stereo|c0=c0|c1=c0", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    print(json.dumps({"channel": ch, "lufs": float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])}))

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], talk="--broll" not in sys.argv)
