#!/usr/bin/env python3
"""Run every local proof."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    proofs = sorted(ROOT.glob("*/*/poc.py"))
    failed = []
    for proof in proofs:
        print(f"== {proof.parent.relative_to(ROOT)}")
        result = subprocess.run([sys.executable, str(proof)], cwd=proof.parent)
        if result.returncode != 0:
            failed.append(str(proof.relative_to(ROOT)))
    print(f"{len(proofs) - len(failed)} of {len(proofs)} passed")
    if failed:
        print("failed:")
        for item in failed:
            print(f"  {item}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
