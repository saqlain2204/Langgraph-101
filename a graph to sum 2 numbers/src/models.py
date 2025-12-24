from pydantic import BaseModel
from typing import Optional

class NumberState(BaseModel):
    value: Optional[float] = None
    valid: Optional[bool] = None

class AdditionState(BaseModel):
    query: str
    num1: NumberState = NumberState()
    num2: NumberState = NumberState()
    result: Optional[float] = None