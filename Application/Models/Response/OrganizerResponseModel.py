from pydantic import BaseModel
from typing import List, Optional


class OrganizerResponseModel(BaseModel):
    Organizers: Optional[List[dict]]
