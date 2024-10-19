import pandas as pd


class Calendar:
    def __init__(self):
        self.event_day = 'EventDay'
        self.initial_date_time = 'InitialDatetime'
        self.final_date_time = 'FinalDatetime'
        self.is_redistributed = 'IsRedistributed'

        self.calendar_df = pd.DataFrame(columns=[self.event_day, self.initial_date_time, self.final_date_time,
                                                 self.is_redistributed])
