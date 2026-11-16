#!/usr/bin/env python3
"""Associates a contact to a company by email domain, then by company name."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    by_domain = {c["domain"].lower(): c["id"] for c in data["companies"]}
    by_name = {c["name"].lower(): c["id"] for c in data["companies"]}
    rows = []
    for contact in data["contacts"]:
        domain = contact["email"].split("@", 1)[1].lower()
        company_id = by_domain.get(domain) or by_name.get(contact.get("company", "").lower())
        rows.append({"email": contact["email"], "company_id": company_id, "matched": bool(company_id)})
    matched = sum(1 for row in rows if row["matched"])
    return {"ok": matched == 2, "summary": f"{matched} of {len(rows)} contacts linked", "rows": rows}


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
