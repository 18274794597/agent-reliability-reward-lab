from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(REPO_ROOT))

from src.runtime.runner import run_eval  # noqa: E402


def main():
    cfg_path = REPO_ROOT / "configs" / "default.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    result, trace_path = run_eval(
        n_tasks=int(cfg["n_eval_tasks"]),
        trace_path=str(REPO_ROOT / cfg["trace_path"]),
        seed=int(cfg["seed"]),
    )

    print(f"[eval] success={result.success}/{result.n_tasks}")
    print(f"[trace] {trace_path}")

if __name__ == "__main__":
    main()
