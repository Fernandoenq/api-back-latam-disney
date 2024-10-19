from pydantic import BaseModel
from typing import List, Optional


class GiftResponseModel(BaseModel):
    Origin: Optional[int]
    Gifts: Optional[List[dict]]

    class Config:
        from_attributes = True
