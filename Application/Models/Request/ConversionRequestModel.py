from Domain.Entities.Conversion import Conversion


class ConversionRequestModel:
    def __init__(self, conversion_request):
        conversion = Conversion()

        self.gift_id = conversion_request[conversion.gift_id]
        self.collect_point_id = conversion_request[conversion.collect_point_id]
        self.event_day = conversion_request[conversion.event_day]
        self.conversion_value = conversion_request[conversion.conversion_value]
        self.conversion_date = conversion_request[conversion.conversion_date]
        self.register_date = conversion_request[conversion.collect_point_person.register_date]
        self.person_name = conversion_request[conversion.collect_point_person.person_name]
        self.cpf = conversion_request[conversion.collect_point_person.cpf]
        self.phone = conversion_request[conversion.collect_point_person.phone]
        self.birth_date = conversion_request[conversion.collect_point_person.birth_date]
        self.mail = conversion_request[conversion.collect_point_person.mail]
