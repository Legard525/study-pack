#!/usr/bin/env bash
# Print a study-pack HTML file to PDF with a headless Chromium-family browser.
# Usage: html_to_pdf.sh <in.html> <out.pdf>
set -eu
in="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"; out="$2"

candidates=(
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  "/Applications/Chromium.app/Contents/MacOS/Chromium"
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
  "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
  google-chrome google-chrome-stable chromium chromium-browser microsoft-edge msedge
  "/c/Program Files/Google/Chrome/Application/chrome.exe"
  "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
)
browser=""
for c in "${candidates[@]}"; do
  if [ -x "$c" ] || command -v "$c" >/dev/null 2>&1; then browser="$c"; break; fi
done
if [ -z "$browser" ]; then
  echo "No Chrome/Chromium/Edge found. Open $in in any browser and print to PDF (A4, no headers)." >&2
  exit 2
fi

# virtual-time-budget lets KaTeX (loaded from a CDN) finish rendering before printing.
"$browser" --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=15000 --run-all-compositor-stages-before-draw \
  --print-to-pdf="$out" "file://$in" 2>/dev/null
[ -s "$out" ] && echo "wrote $out" || { echo "printing failed" >&2; exit 1; }
