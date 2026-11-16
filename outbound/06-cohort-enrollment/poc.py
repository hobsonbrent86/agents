#!/usr/bin/env python3
"""Builds lists from title rules and enrolls people who are not already in a sequence."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for person in data["people"]:
        title = person["title"].lower()
        cohort = next((rule["cohort"] for rule in data["rules"] if rule["title_contains"] in title), None)
        action = "skip" if person["enrolled"] or not cohort else "enroll"
        rows.append({"email": person["email"], "cohort": cohort, "action": action})
    enrolled = sum(1 for row in rows if row["action"] == "enroll")
    return {"ok": enrolled == 1, "summary": f"{enrolled} new enrollments", "rows": rows}


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
