# scripts/build_dataset.py
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List
import sys
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(REPO_ROOT))

from src.tasks.schema import Task, ValidatorSpec  # noqa: E402


def _make_tasks(n: int) -> List[Task]:
    tasks: List[Task] = []

    # A) exact：强约束输出（最适合打可靠性）
    math_pairs = [(7, 5), (12, 9), (33, 8), (19, 6), (100, 23), (41, 1), (9, 9), (58, 7), (6, 44), (17, 3)]
    for i, (a, b) in enumerate(math_pairs[: min(10, n)]):
        gold = str(a + b)
        tasks.append(
            Task(
                id=f"exact_math_{i}",
                input=f"Compute {a}+{b}. Output only the number.",
                allowed_tools=[],
                validator=ValidatorSpec(type="exact", params={"case_sensitive": True}),
                gold=gold,
                meta={"category": "exact", "difficulty": 1, "tags": ["math", "format_strict"]},
            )
        )

    # B) contains：允许自由发挥，但必须包含关键字（后面做 planner/reflect 很常用）
    keywords = [("alpha", "beta"), ("red", "blue"), ("cat", "robot"), ("fast", "safe"), ("trace", "replay")]
    for i, (k1, k2) in enumerate(keywords):
        tasks.append(
            Task(
                id=f"contains_{i}",
                input=f"Write ONE line that contains '{k1}' and '{k2}' (in any order).",
                allowed_tools=[],
                validator=ValidatorSpec(type="contains", params={"needles": [k1, k2]}),
                gold=f"{k1} {k2}",
                meta={"category": "contains", "difficulty": 1, "tags": ["constraint"]},
            )
        )

    # C) regex：格式校验（手机号/日期/ID 这类超典型）
    regex_tasks = [
        ("Return a date in format YYYY-MM-DD for: Dec 29, 2025.", r"\d{4}-\d{2}-\d{2}", "2025-12-29"),
        ("Output a 6-digit numeric code.", r"\d{6}", "123456"),
        ("Output an uppercase 3-letter code.", r"[A-Z]{3}", "ABC"),
        ("Output a signed integer like -12 or 7.", r"-?\d+", "-12"),
        ("Output a hex color like #A1B2C3.", r"#[0-9A-Fa-f]{6}", "#A1B2C3"),
    ]
    for i, (inp, pattern, gold) in enumerate(regex_tasks):
        tasks.append(
            Task(
                id=f"regex_{i}",
                input=inp + " Output only the answer.",
                allowed_tools=[],
                validator=ValidatorSpec(type="regex", params={"pattern": pattern}),
                gold=gold,
                meta={"category": "regex", "difficulty": 2, "tags": ["format"]},
            )
        )

    # D) json_subset：最小 JSON 可靠性（后面接 tool 输出/状态机超好用）
    json_specs: List[Dict[str, object]] = [
        {"a": 1, "b": 2},
        {"name": "miku", "lang": "zh"},
        {"ok": True, "n": 3},
        {"task": "ep_0", "step": 0},
        {"mode": "tool_use", "budget": 2},
        {"x": "alpha", "len": 5},
        {"city": "Denver", "temp": 18},
        {"retry": 3, "backoff": "exp"},
        {"cache": False, "seed": 42},
        {"status": "done", "success": 1},
    ]
    for i, expected in enumerate(json_specs):
        gold = json.dumps(expected, ensure_ascii=False)
        tasks.append(
            Task(
                id=f"json_subset_{i}",
                input=f"Return a JSON object that includes these exact key-values: {expected}. Output JSON only.",
                allowed_tools=[],
                validator=ValidatorSpec(type="json_subset", params={"expected": expected}),
                gold=gold,
                meta={"category": "json", "difficulty": 2, "tags": ["json", "format_strict"]},
            )
        )

    # 控制数量到 n（我们默认会产出 10 + 5 + 5 + 10 = 30 条左右）
    return tasks[:n]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="data/tasks.jsonl")
    parser.add_argument("--n", type=int, default=40)
    args = parser.parse_args()

    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    tasks = _make_tasks(args.n)

    with out_path.open("w", encoding="utf-8") as f:
        for t in tasks:
            f.write(json.dumps(t.to_dict(), ensure_ascii=False) + "\n")

    print(f"[build_dataset] wrote {len(tasks)} tasks -> {out_path}")


if __name__ == "__main__":
    main()
