#!/usr/bin/env python

import argparse
from contextlib import contextmanager
import sys
import enum
from dataclasses import dataclass

class State(enum.Enum):
    """
    State used by the parser
    """
    INIT = enum.auto()
    DESC = enum.auto()
    EXAMPLE = enum.auto()
    SCOPE = enum.auto()
    TARGET = enum.auto()

@dataclass
class Entry:
    """
    Entry stores the information used.
    """
    name: str = ""
    desc: str = ""
    example: str = ""
    scope: str = ""
    target: str = ""

    def set_name_desc(self, desc_line):
        """
        set_name_desc is a helper method to set both from the description line.
        """
        self.name, self.desc = desc_line.split(" - ", maxsplit=1)

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
    state = State.INIT
    entry = Entry()
    for line in infile:
        match state:
            case State.INIT:
                if line == "--------------------\n":
                    state = State.DESC
            case State.DESC:
                if line != "\n":
                    entry.set_name_desc(line)
                    state = State.EXAMPLE
            case State.EXAMPLE:
                if line.startswith("Supported Scopes: "):
                    entry.scope = line[len("Supported Scopes: "):]
                    state = State.SCOPE
                else:
                    entry.example += line
            case State.SCOPE:
                if line.startswith("Supported Target: "):
                    entry.scope = line[len("Supported Target: "):]
                state = State.INIT
                print(entry)
            case _:
                pass
