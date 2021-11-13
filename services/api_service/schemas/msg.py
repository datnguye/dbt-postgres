from typing import Optional
from pydantic import BaseModel

class Msg(BaseModel):
    msg: str

class TaskMsg(BaseModel):
    taskid: str
    msg: str

class TaskState(BaseModel):
    code: int
    msg: Optional[str]
    result: Optional[str]