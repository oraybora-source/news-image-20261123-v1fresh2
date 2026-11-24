#!/usr/bin/env python3
"""news-image-20261123 V1fresh2 entrypoint (Python 3.13, standard library only).

The front page (a 1024x1024 PNG) was drawn in this session by render.py
and is shipped in this repository as entry.png. This program only copies
those bytes to the output directory, so two runs are byte-identical and
it needs no network, no clock and no randomness.

Run it the way the harness does:
    python3 main.py            # writes /output/entry.png
or, outside the harness:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if _sha256(dst) != _sha256(src):
        raise SystemExit("entry.png copy is not byte-identical")
    os.chmod(dst, 0o644)
    os.chmod(out_dir, 0o755)


if __name__ == "__main__":
    main()
