from pydantic import BaseModel
from typing import List, Optional


class ResidueResponseModel(BaseModel):
    Residues: Optional[List[dict]]

    class Config:
        from_attributes = True
