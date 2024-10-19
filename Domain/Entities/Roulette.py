import pandas as pd
from Domain.Entities.Organizer import Organizer


class Roulette:
    def __init__(self):
        self.roulette_id = 'RouletteId'
        self.roulette_name = 'RouletteName'
        self.starting_inventory = 'StartingInventory'

        self.roulette_df = pd.DataFrame(columns=[self.roulette_id, self.roulette_name, self.starting_inventory])
