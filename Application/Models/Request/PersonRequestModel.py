from Domain.Entities.Person import Person


class PersonRequestModel:
    def __init__(self, person_request):
        roulette_person = Person()
        self.register_date = person_request[roulette_person.register_date]
        self.person_name = person_request[roulette_person.person_name]
        self.cpf = person_request[roulette_person.cpf]
        self.phone = person_request[roulette_person.phone]
        self.birth_date = person_request[roulette_person.birth_date]
        self.mail = person_request[roulette_person.mail]
