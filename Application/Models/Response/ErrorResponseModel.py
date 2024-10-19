from typing import List
from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    Errors: List[str]
