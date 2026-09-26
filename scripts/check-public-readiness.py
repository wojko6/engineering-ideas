#!/usr/bin/env python3
"""Fail CI on common public-repository hygiene mistakes.

This is intentionally a lightweight guard, not a secret-scanning guarantee.
Human review remains required.
"""

from __future__ import annotations

import ipaddress
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

REQUIRED = {
    "README.md",
    "BACKLOG.md",
    "PUBLICATION.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "LICENSE",
}

FORBIDDEN_SUFFIXES = {
    ".pcap",
    ".pcapng",
    ".cap",
    ".har",
    ".key",
    ".pem",
    ".p12",
    ".pfx",
    ".ovpn",
    ".sqlite",
    ".sqlite3",
    ".db",
}

TOKEN_PATTERNS = {
    "private-key header": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "Tailscale auth key": re.compile(r"\btskey-[A-Za-z0-9_-]{8,}\b"),
    "GitHub token": re.compile(
        r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"
    ),
    "MAC address": re.compile(r"\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b"),
    "UUID-like identifier": re.compile(
        r"\b[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[1-5][0-9A-Fa-f]{3}-"
        r"[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}\b"
    ),
    "deployment username": re.compile(r"\b(?:admin1|wojciech)\b", re.IGNORECASE),
    "DDNS hostname": re.compile(r"\b[A-Za-z0-9.-]+\.asuscomm\.com\b", re.IGNORECASE),
    "absolute home path": re.compile(r"/home/[A-Za-z0-9._-]+/"),
}

EMAIL_RE = re.compile(r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
IPV4_RE = re.compile(r"(?<![0-9.])(?:\d{1,3}\.){3}\d{1,3}(?![0-9.])")
IPV6_CANDIDATE_RE = re.compile(r"(?<![0-9A-Fa-f:])(?:[0-9A-Fa-f]{0,4}:){2,}[0-9A-Fa-f]{0,4}(?![0-9A-Fa-f:])")
MD_LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")

ALLOWED_EMAIL_DOMAINS = {
    "example.com",
    "example.org",
    "example.net",
    "users.noreply.github.com",
    "github.com",
}

DOC_V4 = (
    ipaddress.ip_network("192.0.2.0/24"),
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("203.0.113.0/24"),
)
LOOPBACK_V4 = ipaddress.ip_network("127.0.0.0/8")

FORBIDDEN_V4 = (
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("100.64.0.0/10"),
)


def tracked_files() -> list[Path]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "-z"], text=False
    )
    return [ROOT / p.decode("utf-8") for p in raw.split(b"\0") if p]


def is_probably_text(path: Path) -> bool:
    try:
        data = path.read_bytes()
    except OSError:
        return False
    return b"\0" not in data[:8192]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def check_required(files: list[Path], failures: list[str]) -> None:
    rels = {p.relative_to(ROOT).as_posix() for p in files}
    for name in sorted(REQUIRED - rels):
        fail(f"missing required public-readiness file: {name}", failures)


def check_file_types(files: list[Path], failures: list[str]) -> None:
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"forbidden raw/sensitive artifact is tracked: {rel}", failures)
        if any(part in {"private", "secrets"} for part in path.parts):
            fail(f"private/secrets path is tracked: {rel}", failures)


def check_text(path: Path, failures: list[str]) -> None:
    if path.resolve() == SELF:
        return

    rel = path.relative_to(ROOT).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return

    for name, pattern in TOKEN_PATTERNS.items():
        if pattern.search(text):
            fail(f"{rel}: found {name}", failures)

    for email in EMAIL_RE.findall(text):
        domain = email.rsplit("@", 1)[1].lower()
        if domain not in ALLOWED_EMAIL_DOMAINS:
            fail(f"{rel}: non-example email address found: {email}", failures)

    for candidate in IPV4_RE.findall(text):
        try:
            ip = ipaddress.ip_address(candidate)
        except ValueError:
            continue
        if ip == ipaddress.ip_address("0.0.0.0") or ip in LOOPBACK_V4:
            continue
        if any(ip in net for net in DOC_V4):
            continue
        if any(ip in net for net in FORBIDDEN_V4):
            fail(f"{rel}: deployment-like private/tailnet IPv4 found: {candidate}", failures)
        elif not ip.is_multicast:
            fail(
                f"{rel}: real/non-documentation IPv4 found: {candidate}; "
                "use an abstract label or RFC 5737 example",
                failures,
            )

    for candidate in IPV6_CANDIDATE_RE.findall(text):
        if candidate in {"::", "::1"}:
            continue
        try:
            ip = ipaddress.ip_address(candidate)
        except ValueError:
            continue
        if ip in ipaddress.ip_network("2001:db8::/32"):
            continue
        fail(
            f"{rel}: non-documentation IPv6 found: {candidate}; "
            "use 2001:db8::/32 or an abstract label",
            failures,
        )


def check_markdown_links(path: Path, failures: list[str]) -> None:
    if path.suffix.lower() != ".md":
        return
    rel = path.relative_to(ROOT).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return

    for raw in MD_LINK_RE.findall(text):
        target = raw.strip().strip("<>")
        if not target:
            continue

        # Optional Markdown title after a path is outside the path itself.
        if " " in target and not target.startswith(("http://", "https://")):
            target = target.split(" ", 1)[0]

        lowered = target.lower()
        if lowered.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        if target.startswith("#"):
            continue

        target = unquote(target.split("#", 1)[0])
        if not target:
            continue

        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"{rel}: relative link escapes repository: {raw}", failures)
            continue

        if not resolved.exists():
            fail(f"{rel}: broken relative link: {raw}", failures)


def main() -> int:
    failures: list[str] = []
    files = tracked_files()

    check_required(files, failures)
    check_file_types(files, failures)

    for path in files:
        if not is_probably_text(path):
            continue
        check_text(path, failures)
        check_markdown_links(path, failures)

    if failures:
        print("PUBLIC READINESS: FAIL")
        for item in failures:
            print(f" - {item}")
        return 1

    print(f"PUBLIC READINESS: PASS ({len(files)} tracked files checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
