from Domain.Entities.Report import Report


class ReportRequestModel:
    def __init__(self, report_request):
        report = Report()

        self.cpf = report_request[report.cpf]
        self.collect_point_id = report_request[report.collect_point_id]
        self.report_date = report_request[report.report_date]
        self.report_description = report_request[report.report_description]
