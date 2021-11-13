from typing import List
from pydantic import BaseModel



class DbtArgs(BaseModel):
    value: str


class DbtKWArgs(BaseModel):
    key: str
    value: str


class DbtArgument(BaseModel):
    action: str
    args: List[DbtArgs] = []
    kwargs: List[DbtKWArgs] = []