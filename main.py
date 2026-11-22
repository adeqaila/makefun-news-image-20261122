"""Entrypoint for the 22 Nov newspaper-image entry.

The newspaper picture itself is already rendered during the build step
(see compose.py); at grading time this script only has to place a copy
of that finished picture where the grader expects it. It looks for
``entry.png`` sitting beside this file, creates the destination folder
when needed, and copies the image there unchanged.
"""

import os
import shutil
import sys


def _destination_dir():
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if wanted:
        return wanted
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(os.getcwd(), "out")


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(folder, "entry.png")
    target_dir = _destination_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    size = os.path.getsize(target)
    print(f"Wrote {target} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
