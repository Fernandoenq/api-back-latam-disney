import pandas as pd
import numpy as np
from Domain.Entities.Roulette import Roulette
from Domain.Entities.Gift import Gift
from Domain.Entities.Person import Person
from Domain.Entities.Calendar import Calendar


class Award:
    def __init__(self):
        self.award_id = 'AwardId'
        self.roulette_id = 'RouletteId'
        self.gift_id = 'GiftId'
        self.person_id = 'PersonId'
        self.award_status = 'AwardStatus'
        self.predefined_datetime = 'PredefinedDateTime'
        self.award_date = 'AwardDate'
        self.event_day = 'EventDay'
        self.is_updated = 'IsUpdated'
        self.roulette = Roulette()
        self.gift = Gift()
        self.roulette_person = Person()
        self.calendar = Calendar()

        self.award_df = pd.DataFrame(columns=[self.award_id, self.roulette_id, self.gift_id, self.person_id,
                                              self.award_status, self.predefined_datetime, self.award_date,
                                              self.event_day, self.is_updated])

    def to_map(self, award_df: pd.DataFrame) -> pd.DataFrame:
        award_df[self.roulette_id] = award_df[self.roulette_id].astype(str)
        award_df[self.gift_id] = award_df[self.gift_id].astype(int).astype(str)
        award_df[self.predefined_datetime] = award_df[self.predefined_datetime].astype(str)
        award_df[self.event_day] = award_df[self.event_day].astype(str)
        award_df[self.is_updated] = award_df[self.is_updated].astype(str)

        return award_df.replace(np.nan, None)
