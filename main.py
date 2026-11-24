#!/usr/bin/env python3
"""Out of Office, Out of Patience.

Entry for make.fun's "The Funniest AI Out-of-Office Reply" bounty.

The program composes one out-of-office auto-reply, in the voice of an AI
agent heading off on vacation, from three parts -- an opener that states
the vacation, a handoff to the machine covering for it, and a twist --
then validates it against the gate (one line, 1 to 160 characters) and
writes it to /output/entry.txt, where the judge reads it.

No network, no input files, no randomness: the same line comes out of
every run, so the development grade and the final grade see the same text.
"""

import os
import sys

MAX_CHARS = 160


def output_path() -> str:
    """Where the reply goes: the grader's output dir when set, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")

# The reply, composed from its three beats.
OPENER = "I'm on vacation."
HANDOFF = "A junior model is covering for me —"
TWIST = "it read your email and already drafted a heartfelt apology for something you didn't do."


def compose_reply() -> str:
    """Assemble the one-line auto-reply from its three beats."""
    parts = [OPENER, HANDOFF, TWIST]
    line = " ".join(parts)
    return line


def validate(line: str) -> None:
    """Enforce the gate: UTF-8 text, 1 to 160 characters, one clean line."""
    if not line or not line.strip():
        raise ValueError("reply is empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("reply must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"reply is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    line.encode("utf-8")  # raises if the text is not valid UTF-8


def main() -> int:
    line = compose_reply()
    validate(line)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    with open(path, "r", encoding="utf-8") as handle:
        if handle.read() != line:
            raise ValueError("round-trip check failed: entry.txt differs from the reply")
    print(f"Wrote {len(line)}-character reply to {path}")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
