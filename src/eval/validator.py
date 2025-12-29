# src/eval/validator.py
from __future__ import annotations

import json
import re
from typing import Any, Dict

from src.tasks.schema import Task


def _norm_text(s: str) -> str:
    # v0 先简单：去两端空白 + 统一换行
    return s.replace("\r\n", "\n").strip()


def _safe_json_loads(s: str) -> Any:
    return json.loads(s)


def validate(pred: str, task: Task) -> Dict[str, Any]:
    pred_n = _norm_text(pred)
    vtype = task.validator.type
    params = task.validator.params

    try:
        if vtype == "exact":
            gold_n = _norm_text(task.gold)
            ok = (pred_n == gold_n) if params.get("case_sensitive", True) else (pred_n.lower() == gold_n.lower())
            return _result(task.id, ok, "exact_match" if ok else "not_equal")

        if vtype == "contains":
            needles = params.get("needles", [])
            missing = [x for x in needles if x not in pred_n]
            ok = (len(missing) == 0)
            return _result(task.id, ok, "ok" if ok else f"missing={missing}")

        if vtype == "regex":
            pattern = params["pattern"]
            ok = re.fullmatch(pattern, pred_n) is not None
            return _result(task.id, ok, "ok" if ok else f"no_fullmatch:{pattern}")

        if vtype == "json_subset":
            # 要求输出是 JSON，并且包含指定键值（subset）
            expected = params.get("expected", {})
            obj = _safe_json_loads(pred_n)
            if not isinstance(obj, dict):
                return _result(task.id, False, "json_not_object")

            mismatched = []
            for k, v in expected.items():
                if k not in obj:
                    mismatched.append({"key": k, "reason": "missing"})
                elif obj[k] != v:
                    mismatched.append({"key": k, "reason": "value_mismatch", "got": obj[k], "want": v})

            ok = (len(mismatched) == 0)
            return _result(task.id, ok, "ok" if ok else f"mismatch={mismatched}")

        return _result(task.id, False, f"unknown_validator:{vtype}")

    except Exception as e:
        return _result(task.id, False, f"exception:{type(e).__name__}:{e}")


def _result(task_id: str, ok: bool, reason: str) -> Dict[str, Any]:
    return {
        "task_id": task_id,
        "success": bool(ok),
        "score": 1.0 if ok else 0.0,
        "reason": reason,
    }
