#!/usr/bin/env python3
"""Verify every exact realization certificate with rational arithmetic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verification.rationalize import CertificateError, display_path, verify_certificate


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--certificates",
        type=Path,
        default=repo_root / "gallery" / "certificates",
        help="certificate root",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]
    certificate_root = args.certificates.resolve()
    certificates = sorted(certificate_root.rglob("*.json"))
    failures = 0
    for certificate in certificates:
        try:
            source = verify_certificate(certificate, certificate_root, repo_root)
            print(
                f"[valid] {display_path(certificate, repo_root)} -> "
                f"{display_path(source, repo_root)}"
            )
        except (CertificateError, OSError, ValueError) as exc:
            failures += 1
            print(f"[invalid] {certificate}: {exc}", file=sys.stderr)
    print(f"Verified {len(certificates) - failures}/{len(certificates)} certificates")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
