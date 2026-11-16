#!/usr/bin/env python3
"""Fills a missing phone from the company record, then from a local lookup table."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    company_phone = {c["domain"]: c["phone"] for c in data["companies"]}
    lookup = {c["domain"]: c["phone"] for c in data["lookup"]}
    rows = []
    for contact in data["contacts"]:
        domain = contact["email"].split("@", 1)[1]
        phone = contact.get("phone") or company_phone.get(domain) or lookup.get(domain) or ""
        source = "contact" if contact.get("phone") else "company" if domain in company_phone else "lookup" if domain in lookup else "missing"
        rows.append({"email": contact["email"], "phone": phone, "source": source})
    filled = sum(1 for row in rows if row["phone"])
    return {"ok": filled == 3, "summary": f"{filled} phones present", "rows": rows}


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
