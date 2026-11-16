#!/usr/bin/env python3
"""Ties anonymous visits to known contacts by email, then by company domain."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    by_email = {c["email"]: c for c in data["contacts"]}
    account_by_domain = {a["domain"]: a["id"] for a in data["accounts"]}
    rows = []
    for visit in data["visits"]:
        contact = by_email.get(visit.get("email") or "")
        account_id = contact["account_id"] if contact else account_by_domain.get(visit.get("domain") or "")
        rows.append({"visit_id": visit["visit_id"], "contact_id": contact["id"] if contact else None, "account_id": account_id})
    matched = sum(1 for row in rows if row["account_id"])
    return {"ok": matched == 2, "summary": f"{matched} of {len(rows)} visits matched", "rows": rows}


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
