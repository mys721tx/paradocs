#!/usr/bin/env python

import argparse
from contextlib import contextmanager
import sys

parser = argparse.ArgumentParser(
    description="Format Paradox script documentations."
)

parser.add_argument(
    "--input",
    "-i",
    default=None,
    help="Input file, default to stdin"
)
parser.add_argument(
    "--output",
    "-o",
    default=None,
    help="Output file, default to stdout"
)


@contextmanager
def stream(arg, mode="r", encoding="unicode_escape"):
    """steam simplify"""
    if mode not in ("r", "w"):
        raise ValueError("mode not r or w")
    if arg:
        with open(arg, mode, encoding=encoding) as file:
            yield file
    else:
        yield sys.stdin if mode == "r" else sys.stdout


args = parser.parse_args()

with stream(args.input) as infile:
    for line in infile:
        print(line)
