"""Build WOFF and WOFF2 from the canonical TTF without changing its content."""

import sys
from pathlib import Path

from fontTools.ttLib import TTFont


def main() -> None:
    source, woff, woff2 = map(Path, sys.argv[1:])
    for target, flavor in ((woff, "woff"), (woff2, "woff2")):
        target.parent.mkdir(parents=True, exist_ok=True)
        font = TTFont(source, recalcTimestamp=False)
        font.flavor = flavor
        font.save(target)
        font.close()


if __name__ == "__main__":
    main()
