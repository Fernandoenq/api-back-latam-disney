from pydantic import BaseModel
from typing import Dict, List, Any
import pandas as pd
from Domain.Entities.Conversion import Conversion
from Domain.Entities.Distribution import Distribution


class Resume(BaseModel):
    GiftName: str
    StartingInventory: int
    ConversionMade: int
    OutgoingTransferred: int
    IncomingTransferred: int
    CurrentInventory: int


class GiftAmountByCollectPointResponseModel:
    @staticmethod
    def conversion_dashboard_df_to_json(dashboard_df: pd.DataFrame) -> List[Dict[str, Any]]:
        conversion = Conversion()
        distribution = Distribution()

        result = []
        collect_points = dashboard_df[conversion.collect_point_id].unique()

        for collect_point_id in collect_points:
            collect_point_gifts = []
            collect_point_rows = dashboard_df[dashboard_df[conversion.collect_point_id] == collect_point_id]

            collect_point_name = collect_point_rows[conversion.collect_point.collect_point_name].iloc[0]

            for _, row in collect_point_rows.iterrows():
                gift = {
                    "GiftName": row[conversion.gift.gift_name],
                    "Consolidated": {
                        "CurrentInventory": int(row[distribution.current_inventory]),
                        "ConversionMade": int(row['ConversionMade']),
                        "OutgoingTransferred": int(row['OutgoingTransferred']),
                        "IncomingTransferred": int(row['IncomingTransferred']),
                        "StartingInventory": int(row[distribution.starting_inventory])
                    }
                }
                collect_point_gifts.append(gift)

            result.append({
                "CollectPointName": collect_point_name,
                "Gifts": collect_point_gifts
            })

        return result
