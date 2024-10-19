import pandas as pd
from Domain.Entities.CollectPoint import CollectPoint
from Domain.Entities.CollectPointPerson import CollectPointPerson
from Domain.Entities.Calendar import Calendar
from Domain.Entities.Gift import Gift


class Conversion:
    def __init__(self):
        self.conversion_id = 'ConversionId'
        self.collect_point_id = 'CollectPointId'
        self.person_id = 'PersonId'
        self.event_day = 'EventDay'
        self.gift_id = 'GiftId'
        self.conversion_value = 'ConversionValue'
        self.conversion_date = 'ConversionDate'
        self.collect_point = CollectPoint()
        self.collect_point_person = CollectPointPerson()
        self.calendar = Calendar()
        self.gift = Gift()

        self.conversion_df = pd.DataFrame(columns=[self.conversion_id,  self.collect_point_id,
                                                   self.person_id, self.event_day, self.gift_id, self.conversion_value,
                                                   self.conversion_date])
