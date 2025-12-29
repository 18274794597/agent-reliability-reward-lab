# scripts/check_dataset.py
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(REPO_ROOT))

from src.tasks.schema import Task  # noqa: E402
from src.eval.validator import validate  # noqa: E402


def load_jsonl(p: Path):
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def main():
    path = REPO_ROOT / "data/tasks.jsonl"
    tasks = [Task.from_dict(x) for x in load_jsonl(path)]

    ok = 0
    for t in tasks:
        r = validate(t.gold, t)
        ok += int(r["success"])
        if not r["success"]:
            print("[FAIL]", t.id, r)
            return

    print(f"[check_dataset] {ok}/{len(tasks)} gold passed ✅")


if __name__ == "__main__":
    main()
