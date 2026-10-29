#!/bin/zsh
# CapCut (Mac) draws a BLACK box behind ProRes 4444 alpha (ffmpeg prores_ks) and behind avconvert's
# "HEVC with alpha" preset. It honors HEVC-with-alpha from VideoToolbox (hvc1). Convert every alpha overlay.
# usage: to_hevc_alpha.sh <src_dir_or_file> <dest_dir>
src="$1"; dst="$2"; mkdir -p "$dst"
if [ -d "$src" ]; then files=("$src"/*.mov); else files=("$src"); fi
for f in "${files[@]}"; do
  b=$(basename "$f")
  ffmpeg -nostdin -v error -y -i "$f" -an -c:v hevc_videotoolbox -alpha_quality 0.95 -pix_fmt bgra -b:v 12M -tag:v hvc1 "$dst/${b%.*}.mov" && echo "ok $b"
done
