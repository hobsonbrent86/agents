#!/usr/bin/env python3
"""Lists devices whose app install failed, with the error code."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    rows = [row for row in data["devices"] if row["state"] == "failed"]
    return {"ok": len(rows) == 1 and rows[0]["error"].startswith("0x"), "summary": f"{len(rows)} failed installs", "rows": rows}


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
