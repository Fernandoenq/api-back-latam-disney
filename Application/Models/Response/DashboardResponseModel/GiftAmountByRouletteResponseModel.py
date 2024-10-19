from pydantic import BaseModel
from typing import Dict, List, Any
import pandas as pd
from Domain.Entities.Award import Award


class Resume(BaseModel):
    GiftName: str
    StartingInventory: int
    RescuedAward: int
    LostAward: int
    CurrentInventory: int


class GiftAmountByRouletteResponseModel:
    @staticmethod
    def award_dashboard_df_to_json(dashboard_df: pd.DataFrame) -> List[Dict[str, Any]]:
        award = Award()

        result = []
        roulettes = dashboard_df[award.roulette_id].unique()

        for roulette_id in roulettes:
            roulette_gifts = []
            roulette_rows = dashboard_df[dashboard_df[award.roulette_id] == roulette_id]

            roulette_name = roulette_rows[award.roulette.roulette_name].iloc[0]

            for _, row in roulette_rows.iterrows():
                gift = {
                    "GiftName": row[award.gift.gift_name],
                    "Consolidated": {
                        "CurrentInventory": int(row['CurrentInventory']),
                        "LostAward": int(row['LostAward']),
                        "RescuedAward": int(row['RescuedAward']),
                        "StartingInventory": int(row[award.gift.starting_inventory])
                    }
                }
                roulette_gifts.append(gift)

            result.append({
                "RouletteName": roulette_name,
                "Gifts": roulette_gifts
            })

        return result
