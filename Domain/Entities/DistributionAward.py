import pandas as pd
from Domain.Entities.Roulette import Roulette
from Domain.Entities.Gift import Gift
from Domain.Entities.Calendar import Calendar


class DistributionAward:
    def __init__(self):
        self.roulette_id = 'RouletteId'
        self.gift_id = 'GiftId'
        self.event_day = 'EventDay'
        self.starting_inventory = 'StartingInventory'
        self.roulette = Roulette()
        self.gift = Gift()
        self.calendar = Calendar()

        self.award_df = pd.DataFrame(columns=[self.roulette_id, self.gift_id, self.event_day, self.starting_inventory])
