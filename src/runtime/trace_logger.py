from __future__ import annotations

import json
import time
from dataclasses import asdict,dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Union

@dataclass
class TraceStep:
    ts:float
    episode_id : str
    step_id:int
    state:Dict[str,Any]
    action:Dict[str,Any]
    obs:Dict[str,Any]
    cost:Dict[str,Any]
    error:Optional[str] = None


class TraceLogger:
    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
    
    def log_step(self,step:TraceStep) -> None:
        line = json.dumps(asdict(step),ensure_ascii=False)
        with self.path.open("a",encoding = "utf-8") as f:
            f.write(line+ "\n")
    
    @staticmethod
    def now() ->float:
        return time.time()
