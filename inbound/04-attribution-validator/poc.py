#!/usr/bin/env python3
"""Flags conversions that have no matching click, and totals the spend sitting on those campaigns."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    clicks = set(data["clicks"])
    ghosts = []
    for conv in data["conversions"]:
        click_id = conv.get("click_id")
        if not click_id or click_id not in clicks:
            ghosts.append(conv)
    ghost_campaigns = {row["campaign"] for row in ghosts}
    wasted = sum(row["amount"] for row in data["spend"] if row["campaign"] in ghost_campaigns)
    return {
        "ok": len(ghosts) == 2 and wasted == 110,
        "summary": f"{len(ghosts)} ghost conversions, {wasted} spend on those campaigns",
        "rows": ghosts,
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
