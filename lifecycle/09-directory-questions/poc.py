#!/usr/bin/env python3
"""Answers plain questions about MFA and conditional access from a local snapshot."""

from __future__ import annotations

import json
from pathlib import Path

def run(data: dict) -> dict:
    answers = []
    for question in data["questions"]:
        if "mfa" in question:
            names = [user["name"] for user in data["users"] if not user["mfa"]]
            answers.append({"question": question, "answer": names})
        elif "report" in question:
            names = [policy["name"] for policy in data["policies"] if policy["state"] == "report"]
            answers.append({"question": question, "answer": names})
        else:
            answers.append({"question": question, "answer": []})
    return {"ok": answers[0]["answer"] == ["Sam"] and answers[1]["answer"] == ["Block legacy auth"], "summary": f"{len(answers)} questions answered", "rows": answers}


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
