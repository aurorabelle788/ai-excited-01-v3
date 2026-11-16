"""ai-excited-01-v3 entry program.

Copies entry.jpg byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png
(/output by default) and verifies the copy matches the source by size
and sha256. Exits non-zero with an error message on any mismatch.
Standard library only.
"""

import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.jpg")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_jpeg(path):
    """Reject a truncated or non-JPEG source: SOI marker first, EOI last."""
    with open(path, "rb") as handle:
        head = handle.read(2)
        handle.seek(-2, os.SEEK_END)
        tail = handle.read(2)
    if head != b"\xff\xd8":
        print(f"error: {path} does not start with a JPEG SOI marker",
              file=sys.stderr)
        return False
    if tail != b"\xff\xd9":
        print(f"error: {path} does not end with a JPEG EOI marker",
              file=sys.stderr)
        return False
    return True


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(output_dir, "entry.png")

    if not os.path.isfile(SOURCE):
        print(f"error: source image not found: {SOURCE}", file=sys.stderr)
        return 1

    if not check_jpeg(SOURCE):
        return 1

    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(SOURCE, target)

    source_size = os.path.getsize(SOURCE)
    target_size = os.path.getsize(target)
    if source_size != target_size:
        print(
            f"error: size mismatch: source {source_size} bytes, "
            f"output {target_size} bytes",
            file=sys.stderr,
        )
        return 1

    source_hash = sha256_of(SOURCE)
    target_hash = sha256_of(target)
    if source_hash != target_hash:
        print(
            f"error: sha256 mismatch: source {source_hash}, "
            f"output {target_hash}",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {target} ({target_size} bytes, sha256 {target_hash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
