#!/usr/bin/env python3
"""Slot 1 entrypoint — news-image-20261122.

Stdlib only. Copies the entry image this repository holds to the
grader's output directory as entry.png. No network, no drawing at
grade time: the image is produced by compose.py (stdlib + PIL) at
build time, and this program reproduces it byte for byte.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if os.path.isdir("/output") else "out"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
