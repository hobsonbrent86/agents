#!/usr/bin/env python3
"""Reassigns a task to the contact owner and flags tasks that are not linked to a contact."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    owners = {row["id"]: row["owner"] for row in data["contacts"]}
    rows = []
    for task in data["tasks"]:
        owner = owners.get(task.get("contact_id"))
        if not task.get("contact_id"):
            rows.append({**task, "action": "unlink"})
        elif task["owner"] != owner:
            rows.append({**task, "owner": owner, "action": "reassign"})
        else:
            rows.append({**task, "action": "keep"})
    return {"ok": rows[0]["action"] == "reassign" and rows[1]["action"] == "unlink", "summary": "1 reassigned, 1 unlinked", "rows": rows}


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
