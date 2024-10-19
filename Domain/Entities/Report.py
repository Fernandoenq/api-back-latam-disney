import pandas as pd


class Report:
    def __init__(self):
        self.report_id = 'ReportId'
        self.cpf = 'Cpf'
        self.collect_point_id = 'CollectPointId'
        self.report_date = 'ReportDate'
        self.report_description = 'ReportDescription'

        self.report_df = pd.DataFrame(columns=[self.report_id, self.cpf, self.collect_point_id, self.report_date,
                                               self.report_description])
