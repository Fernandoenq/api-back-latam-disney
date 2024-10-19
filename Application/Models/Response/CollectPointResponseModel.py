from pydantic import BaseModel
from typing import List, Optional


class CollectPointResponseModel(BaseModel):
    CollectPoints: Optional[List[dict]]
