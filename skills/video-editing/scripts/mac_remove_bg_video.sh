#!/bin/zsh
# Cut the background out of a video clip with Apple Vision, then encode the one alpha format CapCut (Mac) honors.
# usage: mac_remove_bg_video.sh in.mov out.mov [person|foreground] [fps]
#   person (default) is steadier frame-to-frame for talking heads; foreground handles products/objects.
set -e
in="$1"; out="$2"; mode="${3:-person}"; fps="${4:-30}"
here="${0:A:h}"; work=$(mktemp -d)
ffmpeg -nostdin -v error -i "$in" -vf "fps=$fps" "$work/src_%05d.png"
xcrun swiftc -O "$here/mac_remove_bg.swift" -o "$work/rmbg" 2>/dev/null || true
if [ -x "$work/rmbg" ]; then "$work/rmbg" "$work" "$work/cut" --mode "$mode"; else swift "$here/mac_remove_bg.swift" "$work" "$work/cut" --mode "$mode"; fi
ffmpeg -nostdin -v error -y -framerate "$fps" -i "$work/cut/src_%05d.png" -c:v hevc_videotoolbox -alpha_quality 0.95 -pix_fmt bgra -b:v 12M -tag:v hvc1 "$out"
rm -rf "$work"; echo "wrote $out"
