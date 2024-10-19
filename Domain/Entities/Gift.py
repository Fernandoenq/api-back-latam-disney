import pandas as pd


class Gift:
    def __init__(self):
        self.gift_id = 'GiftId'
        self.gift_name = 'GiftName'
        self.starting_inventory = 'StartingInventory'
        self.origin = 'Origin'

        self.gift_df = pd.DataFrame(columns=[self.gift_id, self.gift_name, self.starting_inventory, self.origin])
