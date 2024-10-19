from pydantic import BaseModel
from typing import List, Optional


class EventDayResponseModel(BaseModel):
    EventDays: Optional[List[dict]]
