#!/usr/bin/env python3
"""Reads a payroll export and totals gross pay, headcount, and the pay date."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    people = data["run"]["employees"]
    gross = sum(person["gross"] for person in people)
    return {
        "ok": gross == 7200 and len(people) == 2,
        "summary": f"{data['company']} payroll {data['run']['pay_date']}: {len(people)} people, gross {gross}",
        "rows": people,
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
