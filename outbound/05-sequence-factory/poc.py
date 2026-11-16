#!/usr/bin/env python3
"""Builds an email, social, and phone sequence from a playbook. A second pass patches the subject on step 1."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    steps = [dict(step) for step in data["steps"]]
    patch = data["patch"]
    target = steps[patch["step"] - 1]
    target.update({key: value for key, value in patch.items() if key != "step"})
    return {
        "ok": len(steps) == 3 and steps[0]["subject"].endswith("ops"),
        "summary": f"{data['name']} has {len(steps)} steps",
        "rows": steps,
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
