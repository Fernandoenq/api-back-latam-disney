import pandas as pd
from Domain.Entities.Organizer import Organizer


class CollectPoint:
    def __init__(self):
        self.collect_point_id = 'CollectPointId'
        self.collect_point_name = 'CollectPointIdName'
        self.starting_inventory = 'StartingInventory'

        self.roulette_df = pd.DataFrame(columns=[self.collect_point_id, self.collect_point_name,
                                                 self.starting_inventory])
