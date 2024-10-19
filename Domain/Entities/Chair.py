import pandas as pd


class Chair:
    def __init__(self):
        self.chair_id = 'ChairId'
        self.chair_name = 'ChairName'

        self.chair_df = pd.DataFrame(columns=[self.chair_id, self.chair_name])
