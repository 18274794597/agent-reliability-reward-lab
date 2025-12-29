from __future__ import annotations

from dataclasses import dataclass
from typing import Any,Dict,List,Literal,Optional

#精准匹配，包含匹配，正则匹配，JSON 子集匹配
ValidatorType = Literal["exact","contains","regex","json_subset"]

@dataclass
class ValidatorSpec:
    type: ValidatorType
    params: Dict[str,Any]


@dataclass
class Task:
    id:str
    input: str
    allowed_tools:List[str]
    validator:ValidatorSpec
    gold:str
    meta:Dict[str,Any]

    @staticmethod
    def from_dict(d:Dict[str,Any]) -> "Task":
        return Task(
            id = d["id"],
            input = d["input"],
            allowed_tools = list(d.get("allowed_tools",[])),
            validator = ValidatorSpec(type=d["validator"]["type"],params=d["validator"].get("params",{})),
            gold = d["gold"],
            meta = dict(d.get("meta",{})),
        )
    
    def to_dict(self) -> Dict[str,Any]:
        return{
            "id":self.id,
            "input":self.input,
            "allowed_tools":self.allowed_tools,
            "validator":{
                "type":self.validator.type,
                "params":self.validator.params,
            },
            "gold":self.gold,
            "meta":self.meta,
        }