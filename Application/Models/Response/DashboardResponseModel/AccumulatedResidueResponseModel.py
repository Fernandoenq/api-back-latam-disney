from pydantic import BaseModel
import pandas as pd
from Domain.Entities.Conversion import Conversion


class Resume(BaseModel):
    CollectPointName: str
    AccumulatedResidue: int


class AccumulatedResidueResponseModel:
    @staticmethod
    def conversion_accumulated_residue_df_to_json(accumulated_residue_df: pd.DataFrame) -> list:
        conversion = Conversion()

        result = []
        for _, row in accumulated_residue_df.iterrows():
            resume = Resume(CollectPointName=row[conversion.collect_point.collect_point_name],
                            AccumulatedResidue=int(row['AccumulatedResidue']))
            result.append(resume.dict())

        return result
