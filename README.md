#Agent Reliabilty & Reward Lab
A minimal lab to evaluate agent reliability with traces, replays, and reward signals(strating from tool-use).

## Quickstart
```bash
python -m src.runtime.runner --n_tasks 1 --trace_path artifacts/traces/trace.jsonl
python scripts/run_eval.py