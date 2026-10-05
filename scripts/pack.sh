#!/bin/sh
# Packs each part folder into dist/<folder>.fzpz, the archive the Fritzing
# app imports: the .fzp and its svg.<view>.*.svg files, flat.
set -e
cd "$(dirname "$0")/.."
mkdir -p dist
for d in */; do
  d=${d%/}
  ls "$d"/part.*.fzp > /dev/null 2>&1 || continue
  rm -f "dist/$d.fzpz"
  (cd "$d" && zip -q -X "../dist/$d.fzpz" part.*.fzp svg.*.svg)
  echo "dist/$d.fzpz"
done
