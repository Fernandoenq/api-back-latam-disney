from pydantic import BaseModel
from typing import List, Optional


class RuleResponseModel(BaseModel):
    Rules: Optional[List[dict]]

    class Config:
        from_attributes = True
