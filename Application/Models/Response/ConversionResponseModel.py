from pydantic import BaseModel
from typing import List, Optional


class ConversionResponseModel(BaseModel):
    Amount: Optional[int]
    Gifts: Optional[List[dict]]

    class Config:
        from_attributes = True
