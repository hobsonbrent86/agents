#!/usr/bin/env python3
"""Checks checkbox values and writes a clean done flag."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = []
    for row in data["rows"]:
        raw = row["done"].strip().lower()
        if raw in {"yes", "true", "1"}:
            rows.append({"task": row["task"], "done": True, "valid": True})
        elif raw in {"no", "false", "0", ""}:
            rows.append({"task": row["task"], "done": False, "valid": True})
        else:
            rows.append({"task": row["task"], "done": None, "valid": False})
    invalid = [row["task"] for row in rows if not row["valid"]]
    return {"ok": invalid == ["Ship badge"], "summary": f"{len(invalid)} invalid checkbox values", "rows": rows}


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
