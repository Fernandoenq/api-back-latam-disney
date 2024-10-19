import pandas as pd


class Turn:
    def __init__(self):
        self.turn_id = 'TurnId'
        self.turn_time = 'TurnTime'

        self.turn_df = pd.DataFrame(columns=[self.turn_id, self.turn_time])
