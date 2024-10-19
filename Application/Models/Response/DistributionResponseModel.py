from pydantic import BaseModel
from typing import Dict
import pandas as pd
from Domain.Entities.Conversion import Conversion
from Domain.Entities.Distribution import Distribution


class Resume(BaseModel):
    GiftId: int
    CurrentInventory: int


class DistributionResponseModel:
    @staticmethod
    def conversion_distribution_df_to_json(dashboard_df: pd.DataFrame) -> list:
        distribution = Distribution()

        result = []
        for _, row in dashboard_df.iterrows():
            resume = Resume(GiftId=row[distribution.gift_id],
                            CurrentInventory=int(row[distribution.current_inventory]))
            result.append(resume.dict())

        return result
