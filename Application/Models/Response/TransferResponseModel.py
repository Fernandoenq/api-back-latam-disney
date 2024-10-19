from pydantic import BaseModel
from typing import List, Optional


class TransferResponseModel(BaseModel):
    Transfers: Optional[List[dict]]
