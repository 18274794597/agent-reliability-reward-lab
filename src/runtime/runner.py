from __future__ import annotations
import argparse
import random
from dataclasses import dataclass
from typing import Dict,List,Tuple

from .trace_logger import TraceLogger,TraceStep

@dataclass
class EvalResult:
    n_tasks: int
    success: int

def run_one_task(task_id:str,logger:TraceLogger,seed:int) -> bool:
    rng = random.Random(seed + int(task_id.split("_")[-1]))

    state = {"task_id":task_id,"goal":"dummy-goal"}
    action = {"type":"THINK","content":"hello trace"}
    obs = {"type":"TEXT","content":"ok"}
    cost = {"tokens":0 , "tool_calls":0}

    step = TraceStep(
        ts = logger.now(),
        episode_id = task_id,
        step_id = 0,
        state = state,
        action = action,
        obs= obs,
        cost = cost,
        error = None,
    )
    logger.log_step(step)
    return rng.random()>0.2

def run_eval(n_tasks:int,trace_path:str,seed:int) -> Tuple[EvalResult,str]:
    logger = TraceLogger(trace_path)

    success = 0
    for i in range(n_tasks):
        task_id = f"ep_{i}"
        ok = run_one_task(task_id,logger,seed = seed)
        success += int(ok)
    return EvalResult(n_tasks = n_tasks,success = success), trace_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace_path",type=str,default="artifacts/traces/trace.jsonl")
    parser.add_argument("--n_tasks",type=int,default=1)
    parser.add_argument("--seed",type=int,default=42)
    args = parser.parse_args()

    print("hello trace")
    result,trace_path = run_eval(args.n_tasks,args.trace_path,args.seed)
    print(f"[done] n_tasks={result.n_tasks} success={result.success} trace={trace_path}")

if __name__ == "__main__":
    main()
