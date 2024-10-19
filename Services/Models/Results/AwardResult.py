from Services.Models.Results.BaseResult import BaseResult
import pandas as pd


class AwardResult(BaseResult):
    result = None
    award_ne_df = pd.DataFrame
