#!/usr/bin/env python3
"""collect_diff.py — 在 review 前打印 diff 的结构化摘要。

用法：
    python3 scripts/collect_diff.py            # 未提交变更（工作树 + 暂存区）
    python3 scripts/collect_diff.py <branch>   # branch..HEAD 范围
    python3 scripts/collect_diff.py <A>..<B>   # commit 范围

输出：Markdown 表格 + Flags 节。非交互、只读 git，不改任何文件。

退出码：0 正常；1 无变更；2 git 调用失败。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

SENSITIVE_PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[=:]\s*[\"'][^\"']{6,}"), "hardcoded secret"),
    (re.compile(r"(?i)aws_secret_access_key"), "AWS secret"),
    (re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"), "private key"),
]

DEBUG_PATTERNS = [
    (re.compile(r"\bTODO\b|\bFIXME\b|\bXXX\b|\bHACK\b"), "TODO/FIXME"),
    (re.compile(r"\bconsole\.log\("), "console.log"),
    (re.compile(r"\bdebugger\s*;"), "debugger"),
    (re.compile(r"\bbreakpoint\(\)"), "breakpoint()"),
    (re.compile(r"\bpdb\.set_trace\("), "pdb.set_trace"),
]


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(f"ERROR: git {' '.join(args)} failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return result.stdout


def resolve_range(spec: str | None) -> tuple[str, list[str]]:
    """返回 (range_label, git diff args)."""
    if not spec:
        return ("uncommitted (working tree + index)", ["diff", "HEAD"])
    if ".." in spec:
        return (spec, ["diff", spec])
    # 当作分支名：merge-base..HEAD
    base = run_git(["merge-base", "HEAD", spec]).strip()
    if not base:
        print(f"ERROR: cannot resolve merge-base with {spec}", file=sys.stderr)
        sys.exit(2)
    return (f"{spec} ({base[:8]}..HEAD)", ["diff", f"{base}..HEAD"])


def parse_numstat(output: str) -> list[tuple[int, int, str]]:
    rows: list[tuple[int, int, str]] = []
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added = 0 if parts[0] == "-" else int(parts[0])
        removed = 0 if parts[1] == "-" else int(parts[1])
        rows.append((added, removed, parts[2]))
    return rows


def scan_flags(diff_text: str) -> dict[str, list[str]]:
    flags: dict[str, list[str]] = {"sensitive": [], "debug": []}
    current_file: str | None = None
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        added = line[1:]
        for pat, label in SENSITIVE_PATTERNS:
            if pat.search(added):
                flags["sensitive"].append(f"{current_file}: {label}")
        for pat, label in DEBUG_PATTERNS:
            if pat.search(added):
                flags["debug"].append(f"{current_file}: {label}")
    return flags


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", nargs="?", help="branch or commit range; default=uncommitted")
    args = parser.parse_args()

    label, diff_args = resolve_range(args.spec)
    numstat_output = run_git([*diff_args, "--numstat"])
    rows = parse_numstat(numstat_output)
    diff_text = run_git([*diff_args])

    if not rows:
        print(f"## Diff Overview\n\n范围: `{label}`\n\n无变更。")
        return 1

    flags = scan_flags(diff_text)
    total_added = sum(r[0] for r in rows)
    total_removed = sum(r[1] for r in rows)

    print("## Diff Overview")
    print()
    print(f"- 范围: `{label}`")
    print(f"- 文件: {len(rows)}")
    print(f"- +{total_added} / -{total_removed}")
    print()
    print("| File | +Added | -Removed |")
    print("|------|--------|----------|")
    for added, removed, path in sorted(rows, key=lambda r: -(r[0] + r[1])):
        print(f"| {path} | {added} | {removed} |")
    print()
    print("## Flags")
    if flags["sensitive"]:
        print("- ⚠️ 疑似敏感信息：")
        for item in flags["sensitive"]:
            print(f"  - {item}")
    else:
        print("- 敏感信息扫描: 无命中")
    if flags["debug"]:
        print("- ⚠️ 调试/TODO 遗留：")
        for item in flags["debug"]:
            print(f"  - {item}")
    else:
        print("- 调试遗留扫描: 无命中")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
