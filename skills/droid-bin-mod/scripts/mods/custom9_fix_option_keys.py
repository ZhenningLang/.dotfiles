#!/usr/bin/env python3
"""Fix Option+Left/Right in Droid 0.69.0.

Verified with external probe on the affected machine:
- Option+Left sends ``\x1bb`` and Bun reports ``meta=true, name="b"``
- Option+Right sends ``\x1bf`` and Bun reports ``meta=true, name="f"``
- Option+Backspace sends ``\x1b\x7f`` and already works through ``backspace`` handling

Root cause:
- In Droid's ``KH(QA,bA)`` meta branch, word-left / word-right check ``QA`` only:
  ``if(QA==="b")...`` and ``if(QA==="f")...``
- On 0.69.0 the parsed event can arrive with ``bA.name`` set while ``QA`` is empty,
  so Option+Left/Right do nothing even though Bun recognized the key correctly

Fix:
- Make the checks fall back to ``bA.name``: ``(QA||bA.name)=="b"`` / ``"f"``
- Keep the patch equal-size by converting two obsolete exploratory no-op blocks
  into slightly shorter compensation comments
"""

import os
import sys

DROID_PATH = os.path.expanduser("~/.local/bin/droid")

LEFT_COMP = b'0/*left via KH*/;        '

RIGHT_COMP = b'0/*right via KH*/;       '

BF_LEFT_OLD = b'if(QA==="b")return Q(),!0;'
BF_LEFT_NEW = b'if((QA||bA.name)=="b")return Q(),!0;'

BF_RIGHT_OLD = b'if(QA==="f")return z(),!0;'
BF_RIGHT_NEW = b'if((QA||bA.name)=="f")return z(),!0;'


def replace_once(data: bytes, old: bytes, new: bytes, label: str) -> tuple[bytes, int]:
    if new in data:
        print(f"  {label}: already applied")
        return data, 0
    pos = data.find(old)
    if pos == -1:
        raise ValueError(f"{label}: anchor not found")
    diff = len(new) - len(old)
    print(f"  {label}: patched at offset {pos} ({diff:+d} bytes)")
    return data[:pos] + new + data[pos + len(old):], diff


def replace_one_of(data: bytes, olds: list[bytes], new: bytes, label: str) -> tuple[bytes, int]:
    if new in data:
        print(f"  {label}: already applied")
        return data, 0
    for old in olds:
        pos = data.find(old)
        if pos != -1:
            diff = len(new) - len(old)
            print(f"  {label}: patched at offset {pos} ({diff:+d} bytes)")
            return data[:pos] + new + data[pos + len(old):], diff
    raise ValueError(f"{label}: no matching anchor found")


def main():
    with open(DROID_PATH, 'rb') as f:
        data = f.read()
    total_diff = 0

    data, diff = replace_once(data, BF_LEFT_OLD, BF_LEFT_NEW, 'option+b fallback via key.name')
    total_diff += diff

    data, diff = replace_once(data, BF_RIGHT_OLD, BF_RIGHT_NEW, 'option+f fallback via key.name')
    total_diff += diff

    data, diff = replace_one_of(
        data,
        [b'0/*opt-left via KH after GH*/;     ', LEFT_COMP],
        LEFT_COMP,
        'left compensation marker',
    )
    total_diff += diff

    data, diff = replace_one_of(
        data,
        [b'0/*opt-right via KH after GH*/;    ', RIGHT_COMP],
        RIGHT_COMP,
        'right compensation marker',
    )
    total_diff += diff

    if total_diff != 0:
        raise ValueError(f"net size drift: {total_diff:+d} bytes")

    with open(DROID_PATH, 'wb') as f:
        f.write(data)

    print("\ncustom9: Done!")
    print("  KH(QA,bA) now falls back to key.name for Option+b / Option+f")
    print("  Option+Backspace remains unchanged")


if __name__ == "__main__":
    main()
