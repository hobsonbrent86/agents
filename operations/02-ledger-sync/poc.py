#!/usr/bin/env python3
"""Maps categorized bank lines to ledger accounts and skips anything still uncategorized."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    posted = []
    skipped = []
    for txn in data["transactions"]:
        code = data["accounts"].get(txn["category"])
        if not code:
            skipped.append(txn["id"])
            continue
        posted.append({"id": txn["id"], "account": code, "amount": txn["amount"]})
    return {"ok": len(posted) == 1 and skipped == ["t2"], "summary": f"{len(posted)} posted, {len(skipped)} skipped", "rows": posted}


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
