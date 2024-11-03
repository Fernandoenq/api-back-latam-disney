import pandas as pd
from Domain.Entities.Person import Person
from Application.Models.Request.PersonRequestModel import PersonRequestModel


class PersonService:
    @staticmethod
    def get_person_by_cpf(cpf: str, cursor) -> pd.DataFrame:
        cursor.execute("Select PersonId, PersonName, Cpf, RegisterDate From Person Where Cpf = %s", (cpf,))
        loaded_person = cursor.fetchall()

        person = Person()
        return pd.DataFrame(loaded_person, columns=[person.person_id, person.person_name, person.cpf,
                                                    person.register_date])

    @staticmethod
    def create_person(person_request: PersonRequestModel, cursor) -> pd.DataFrame:
        cursor.execute("""INSERT INTO Person (PersonName, Cpf, Phone, BirthDate, Mail, CountryName, RegisterDate, 
                            HasAcceptedPromotion, HasAcceptedParticipation) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (person_request.person_name, person_request.cpf, person_request.phone, person_request.birth_date,
                        person_request.mail, person_request.country_name, person_request.register_date,
                        person_request.has_accepted_promotion, person_request.has_accepted_participation))

        return PersonService.get_person_by_cpf(person_request.cpf, cursor)
