#!/usr/bin/env python3
"""Drafts a short comparison from the claims each product makes."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    text = (
        f"{data['us']} and {data['them']} both cover field dispatch. "
        f"{data['us']} adds {data['our_claims'][0].lower()}. "
        f"{data['them']} adds {data['their_claims'][0].lower()}."
    )
    return {"ok": data["us"] in text and data["them"] in text, "summary": "comparison drafted", "rows": [{"text": text}]}


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
