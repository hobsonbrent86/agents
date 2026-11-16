#!/usr/bin/env python3
"""Matches bank lines to ledger lines on date and amount, then lists what is left."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    def key(row):
        return (row["date"], row["amount"])

    bank = list(data["bank"])
    ledger = list(data["ledger"])
    used = set()
    matched = []
    for index, row in enumerate(bank):
        for other_index, other in enumerate(ledger):
            if other_index in used:
                continue
            if key(row) == key(other):
                used.add(other_index)
                matched.append(key(row))
                break
    bank_left = [row for row in bank if key(row) not in matched]
    ledger_left = [row for index, row in enumerate(ledger) if index not in used]
    return {
        "ok": len(matched) == 1 and len(bank_left) == 1 and len(ledger_left) == 1,
        "summary": f"{data['month']}: {len(matched)} matched, {len(bank_left) + len(ledger_left)} open",
        "rows": [{"bank_only": bank_left, "ledger_only": ledger_left}],
    }


def main() -> None:
    fixture = Path(__file__).resolve().parent / "fixtures" / "sample.json"
    data = json.loads(fixture.read_text())
    result = run(data)
    html = result.pop("html", None)
    if html:
        out = Path(__file__).resolve().parent / "out"
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(html)
        result["wrote"] = "out/index.html"
    print(json.dumps(result, indent=2))
    if not result.get("ok"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
