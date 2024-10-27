import pandas as pd


class Person:
    def __init__(self):
        self.person_id = 'PersonId'
        self.person_name = 'PersonName'
        self.cpf = 'Cpf'
        self.phone = 'Phone'
        self.birth_date = 'BirthDate'
        self.mail = 'Mail'
        self.register_date = 'RegisterDate'
        self.has_accepted_promotion = 'HasAcceptedPromotion'
        self.has_accepted_participation = 'HasAcceptedParticipation'

        self.person_df = pd.DataFrame(columns=[self.person_id, self.person_name, self.cpf,
                                               self.phone, self.birth_date, self.mail, self.register_date,
                                               self.has_accepted_promotion, self.has_accepted_participation])
