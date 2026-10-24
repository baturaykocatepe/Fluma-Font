#!/usr/bin/env python3
"""Create the public FLUMA font and specimen download."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import argparse
import hashlib

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "OFL.txt": ROOT / "OFL.txt",
    "SPECIMEN-IMAGE-LICENSE.txt": ROOT / "documentation/image-license.txt",
    "fonts/desktop/Fluma-Regular.ttf": ROOT / "fonts/ttf/Fluma-Regular.ttf",
    "fonts/desktop/Fluma-Regular.otf": ROOT / "fonts/otf/Fluma-Regular.otf",
    "fonts/web/Fluma-Regular.woff": ROOT / "fonts/woff/Fluma-Regular.woff",
    "fonts/web/Fluma-Regular.woff2": ROOT / "fonts/woff2/Fluma-Regular.woff2",
}
FILES.update({
    f"specimens/specimen{i:02d}.png": ROOT / f"documentation/article/specimen{i:02d}.png"
    for i in range(1, 23)
})
README = """FLUMA Font
Version 1.000
Designed by Baturay Kocatepe

This package contains FLUMA Regular in desktop and web formats, and all 22
original specimen images in their published sequence.

Install a file from fonts/desktop for desktop applications. Use the files
under fonts/web for websites. For build tools and editable font sources, visit:
https://github.com/baturaykocatepe/Fluma-Font

The font software is licensed under the SIL Open Font License 1.1 (OFL.txt).
The specimen images are separately licensed under CC BY-SA 4.0
(SPECIMEN-IMAGE-LICENSE.txt). The image license does not apply to the font.
"""


def add_bytes(archive, name, data):
    item = ZipInfo(f"Fluma-Font/{name}", date_time=(2026, 10, 24, 0, 0, 0))
    item.compress_type = ZIP_DEFLATED
    item.external_attr = 0o644 << 16
    archive.writestr(item, data, compresslevel=9)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path, help="Output ZIP path")
    args = parser.parse_args()
    missing = [str(path) for path in FILES.values() if not path.is_file()]
    if missing:
        raise SystemExit("Missing package inputs:\n" + "\n".join(missing))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(args.output, "w") as archive:
        add_bytes(archive, "README.txt", README.encode("utf-8"))
        for name, source in FILES.items():
            add_bytes(archive, name, source.read_bytes())
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(f"{args.output} ({args.output.stat().st_size} bytes, SHA-256 {digest})")
    print(f"{len(FILES)} files plus README.txt")


if __name__ == "__main__":
    main()
