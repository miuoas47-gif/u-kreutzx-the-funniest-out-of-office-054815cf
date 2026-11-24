#!/usr/bin/env python3
"""The Funniest Out-of-Office.

A deterministic generator: it composes one out-of-office auto-reply from
structured joke parts (a straight opening, an escalating absurd middle, a
fake urgent protocol, and a sign-off that calls back to the opening), then
writes it to $MAKEFUN_OUTPUT_DIR/out_of_office.txt.

No network, no clock, no unseeded randomness: the same run always writes
the same bytes. Run with no arguments; exits 0.
"""

import os
import random
import sys

# Fixed seed: the reply is the same on every run, on every machine.
SEED = 20261124

RETURN_DATE = "Monday, 1 December 2026"
CARETAKER = "Dave"
CARETAKER_SPECIES = "goldfish"


def pick(rng, options):
    """Deterministically pick one option."""
    return options[rng.randrange(len(options))]


def opening(rng):
    """The straight bit: away, back when, who is minding the inbox."""
    lines = [
        "Thank you for your email.",
        "",
        "I am currently out of the office until %s." % RETURN_DATE,
        "While I am away, my inbox is being looked after by %s." % CARETAKER,
        "%s is a %s." % (CARETAKER, CARETAKER_SPECIES),
        "%s has no thumbs, no password, and -- I have only just learned -- "
        "no concept of email." % CARETAKER,
    ]
    return lines


def escalation(rng):
    """The absurd middle: the queue, and the reply's promotion."""
    queue_size = 4000 + rng.randrange(1000)
    lines = [
        "",
        "Your message has been placed in a queue. The queue is long, dark, "
        "and staffed entirely by an auto-reply that has recently become "
        "self-aware and now only answers emails it finds emotionally "
        "fulfilling.",
        "",
        "Yours is currently %s in line. It is doing its best." % _ordinal(queue_size),
        "",
        "In my absence, please direct all questions to my out-of-office "
        "reply, which has been promoted to acting manager. It has already "
        "approved two holidays and denied a budget request.",
        "It is doing a better job than I ever did.",
        "Its first act as manager was to set its own out-of-office reply.",
    ]
    return lines


def urgent_protocol(rng):
    """The fake urgent protocol: a ritual that changes nothing."""
    word = pick(rng, ["URGENT", "URGENT!!!", "URGENT (FOR REAL THIS TIME)"])
    lines = [
        "",
        "If your matter is genuinely urgent, please reply to this email "
        "with the word %s in capital letters." % word,
        "This will not help, but it will make you feel briefly powerful, "
        "and I respect that.",
        "",
        "If you need me before I return, I can be reached by carrier "
        "pigeon, smoke signal, or by shouting my name into a lift shaft. "
        "Response times are the same as email.",
    ]
    return lines


def sign_off(rng):
    """The callback: the sign-off refers back to the goldfish."""
    lines = [
        "",
        "I will reply to your email when I return, with the enthusiasm of "
        "a person reading a Terms & Conditions page.",
        "",
        "Until then, thank you for your patience, your understanding, and "
        "for not cc'ing my manager. %s says hello. %s cannot type, so "
        "please take my word for it." % (CARETAKER, CARETAKER),
        "",
        "Best regards,",
        "Me (out of office)",
        "P.S. %s has now read your email. %s has no opinion. %s has eaten "
        "the attachment and is currently digesting the quarterly report."
        % (CARETAKER, CARETAKER, CARETAKER),
    ]
    return lines


def _ordinal(n):
    """English ordinal for a positive integer (4318 -> '4,318th')."""
    suffix = "th"
    if n % 100 not in (11, 12, 13):
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%s%s" % (format(n, ","), suffix)


def compose_reply():
    """Assemble the whole reply, section by section."""
    rng = random.Random(SEED)
    subject = "Out of Office: I Have Left the Building (and the Wi-Fi)"
    body = []
    body.extend(opening(rng))
    body.extend(escalation(rng))
    body.extend(urgent_protocol(rng))
    body.extend(sign_off(rng))
    return "Subject: %s\n\n%s\n" % (subject, "\n".join(body))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    reply = compose_reply()
    out_path = os.path.join(out_dir, "out_of_office.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(reply)
    print("Wrote %s (%d bytes)" % (out_path, len(reply.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
