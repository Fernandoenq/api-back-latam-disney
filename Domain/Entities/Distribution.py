import pandas as pd
import numpy as np
from Domain.Entities.CollectPoint import CollectPoint
from Domain.Entities.Gift import Gift
from Domain.Entities.Calendar import Calendar
from typing import Dict


class Distribution:
    def __init__(self):
        self.distribution_id = 'DistributionId'
        self.collect_point_id = 'CollectPointId'
        self.gift_id = 'GiftId'
        self.event_day = 'EventDay'
        self.starting_inventory = 'StartingInventory'
        self.current_inventory = 'CurrentInventory'
        self.collect_point = CollectPoint()
        self.gift = Gift()
        self.calendar = Calendar()

        self.distribution_df = pd.DataFrame(columns=[self.distribution_id, self.collect_point_id, self.gift_id,
                                                     self.event_day, self.starting_inventory, self.current_inventory])

    def to_map(self, collect_point_id: int, gifts_amount: Dict[str, int]) -> pd.DataFrame:
        gift_ids = list(gifts_amount.keys())
        amounts = list(gifts_amount.values())

        distribution_df = self.distribution_df
        distribution_df[self.gift_id] = gift_ids
        distribution_df[self.gift_id] = distribution_df[self.gift_id].astype(str)
        distribution_df[self.starting_inventory] = amounts
        distribution_df[self.starting_inventory] = distribution_df[self.starting_inventory].astype(str)
        distribution_df[self.current_inventory] = amounts
        distribution_df[self.current_inventory] = distribution_df[self.current_inventory].astype(str)
        distribution_df[self.collect_point_id] = collect_point_id
        distribution_df[self.collect_point_id] = distribution_df[self.collect_point_id].astype(str)

        return distribution_df.replace(np.nan, None)

    def to_map_smaller_quantity(self, collect_point_id, gift_id: int, amount: int) -> pd.DataFrame:
        distribution_df = Distribution().distribution_df
        distribution_df[self.gift_id] = [gift_id]
        distribution_df[self.gift_id] = distribution_df[self.gift_id].astype(str)
        distribution_df[self.starting_inventory] = amount
        distribution_df[self.starting_inventory] = distribution_df[self.starting_inventory].astype(str)
        distribution_df[self.current_inventory] = amount
        distribution_df[self.current_inventory] = distribution_df[self.current_inventory].astype(str)
        distribution_df[self.collect_point_id] = collect_point_id
        distribution_df[self.collect_point_id] = distribution_df[self.collect_point_id].astype(str)

        return distribution_df.replace(np.nan, None)
