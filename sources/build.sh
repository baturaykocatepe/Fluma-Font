#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_dir"

# Pin the build date for byte-identical outputs; override it for a new release.
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1790726400}"

python3 tools/gs2_to_ufo.py sources/Fluma.gs2 sources/Fluma.ufo
fontmake -u sources/Fluma.ufo -o ttf --output-path fonts/ttf/Fluma-Regular.ttf
fontmake -u sources/Fluma.ufo -o otf --output-path fonts/otf/Fluma-Regular.otf
python3 tools/finalize_fonts.py fonts/ttf/Fluma-Regular.ttf fonts/otf/Fluma-Regular.otf
python3 tools/build_webfonts.py fonts/ttf/Fluma-Regular.ttf fonts/woff/Fluma-Regular.woff fonts/woff2/Fluma-Regular.woff2
