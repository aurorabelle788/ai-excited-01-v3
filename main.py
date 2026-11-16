#!/usr/bin/env python3
"""ai-excited-01 v3 entry: a peacock bursting out of a museum tapestry.

Copies the entry image (entry.jpg, a JPEG) byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.png, as the competition requires. The output file
keeps the name entry.png; its JPEG format is told apart by its first bytes.

Validation performed before writing:
  - the source starts with the JPEG SOI marker (FFD8) and ends with EOI (FFD9)
  - a SOF segment parses and reports 1024x1024 pixels

After writing, the output is verified to be byte-identical to the source
(same size and same sha256); any mismatch exits non-zero.
"""

import hashlib
import os
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.jpg")

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def parse_jpeg_dimensions(data):
    """Return (width, height) from the first SOF segment, or None."""
    if len(data) < 4 or data[0:2] != b"\xff\xd8":
        return None
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        if marker == 0xD9:  # EOI
            return None
        if marker == 0xDA:  # SOS: scan data follows, no more headers
            return None
        length = (data[pos + 2] << 8) | data[pos + 3]
        if length < 2 or pos + 2 + length > len(data):
            return None
        if marker in (0xC0, 0xC1, 0xC2):
            height = (data[pos + 5] << 8) | data[pos + 6]
            width = (data[pos + 7] << 8) | data[pos + 8]
            return width, height
        pos += 2 + length
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.png")

    with open(SOURCE, "rb") as f:
        data = f.read()

    if not data.startswith(b"\xff\xd8"):
        print("error: entry.jpg does not start with the JPEG SOI marker", file=sys.stderr)
        return 1
    if not data.endswith(b"\xff\xd9"):
        print("error: entry.jpg does not end with the JPEG EOI marker", file=sys.stderr)
        return 1

    dims = parse_jpeg_dimensions(data)
    if dims is None:
        print("error: could not parse a JPEG SOF segment", file=sys.stderr)
        return 1
    if dims != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"error: expected 1024x1024, got {dims[0]}x{dims[1]}", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)

    with open(out_path, "rb") as f:
        written = f.read()
    if len(written) != len(data):
        print("error: output size differs from entry.jpg", file=sys.stderr)
        return 1
    if not written.startswith(b"\xff\xd8") or not written.endswith(b"\xff\xd9"):
        print("error: output lost its JPEG markers", file=sys.stderr)
        return 1
    if parse_jpeg_dimensions(written) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print("error: output dimensions differ from entry.jpg", file=sys.stderr)
        return 1
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        print("error: output sha256 differs from entry.jpg", file=sys.stderr)
        return 1

    print(f"wrote {out_path} ({len(written)} bytes, sha256 "
          f"{hashlib.sha256(written).hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
