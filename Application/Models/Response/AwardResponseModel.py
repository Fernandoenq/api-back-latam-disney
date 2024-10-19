from pydantic import BaseModel
from typing import List, Optional


class AwardResponseModel(BaseModel):
    Award: Optional[List[dict]]

    class Config:
        from_attributes = True
