#!/usr/bin/env python3
"""Deliver the polished Sunday front page to the grader, byte for byte.

Second entry for make.fun competition news-image-20261122 (@tapetelo):
one 1024x1024 image summing up Sunday 22 November 2026 — 35 stories
in 7 regions, led by the COP31 deal text in Antalya, two tankers hit
leaving the Strait of Hormuz, and the Sparta II ablaze in the Baltic.
This revision keeps the same wire-checked story set as the first
entry and enlarges every headline and brief so the page still reads
when the judge views it at 300 pixels wide.

The finished PNG is bundled beside this script as entry.png. The
grading sandbox installs nothing, so only the standard library is
used. The script copies the bundled picture to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output) and proves the copy
is identical before reporting success.
"""

import hashlib
import os
import struct
import sys

PICTURE = "entry.png"
READ_SIZE = 65536
SIZE_CEILING = 1048576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def script_folder():
    return os.path.dirname(os.path.abspath(__file__))


def output_folder():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def file_digest(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(READ_SIZE)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def png_dimensions(path):
    with open(path, "rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", header[16:24])


def copy_picture(source, target):
    with open(source, "rb") as incoming, open(target, "wb") as outgoing:
        while True:
            block = incoming.read(READ_SIZE)
            if not block:
                break
            outgoing.write(block)


def main():
    source = os.path.join(script_folder(), PICTURE)
    if not os.path.isfile(source):
        print("bundled picture not found: " + source, file=sys.stderr)
        return 1
    if os.path.getsize(source) > SIZE_CEILING:
        print("bundled picture exceeds the 1 MiB ceiling", file=sys.stderr)
        return 1
    dimensions = png_dimensions(source)
    if dimensions != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print("unexpected picture dimensions: %r" % (dimensions,), file=sys.stderr)
        return 1
    folder = output_folder()
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, PICTURE)
    copy_picture(source, target)
    if os.path.getsize(target) != os.path.getsize(source):
        print("incomplete copy at " + target, file=sys.stderr)
        return 1
    if file_digest(target) != file_digest(source):
        print("copy differs from the bundled picture", file=sys.stderr)
        return 1
    print("delivered %s (%d bytes)" % (target, os.path.getsize(target)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
