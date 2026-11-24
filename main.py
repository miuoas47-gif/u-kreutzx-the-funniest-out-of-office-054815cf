#!/usr/bin/env python3
"""The Funniest Out-of-Office: one single-line auto-reply, 140 chars or fewer.

Running this with no arguments prints the line and writes it, alone, to
out.txt inside the output directory (MAKEFUN_OUTPUT_DIR, or ./output).
No randomness, no clock, no network, no input: every run is byte-identical.
"""

import os

LINE = "Out of office: my cat is answering emails now \u2014 she's already approved two refunds and a hostile takeover."


def main() -> int:
    assert "\n" not in LINE and "\r" not in LINE, "the entry must be one line"
    assert len(LINE) <= 140, "the entry must fit in 140 characters"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "out.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")
    print(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
