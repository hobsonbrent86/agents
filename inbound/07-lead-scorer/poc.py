#!/usr/bin/env python3
"""Ranks new contacts from title, company size, and early page views."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    def points(contact):
        title = contact["title"].lower()
        score = 0
        if any(word in title for word in ("vp", "chief", "head")):
            score += 40
        elif "director" in title:
            score += 25
        elif "manager" in title:
            score += 15
        if contact["employees"] >= 200:
            score += 20
        elif contact["employees"] >= 50:
            score += 10
        score += min(contact["views"], 5) * 4
        return score

    rows = []
    for contact in data["contacts"]:
        score = points(contact)
        band = "high" if score >= 60 else "medium" if score >= 30 else "low"
        rows.append({"email": contact["email"], "score": score, "band": band})
    rows.sort(key=lambda row: row["score"], reverse=True)
    return {"ok": rows[0]["email"].startswith("ada@"), "summary": f"top lead {rows[0]['email']} at {rows[0]['score']}", "rows": rows}


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
