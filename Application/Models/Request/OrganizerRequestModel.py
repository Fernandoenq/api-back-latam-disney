from Domain.Entities.Organizer import Organizer


class OrganizerRequestModel:
    def __init__(self, organizer_id: int, organizer_name: str, login: str, secret_key: str):
        self.organizer_id = organizer_id
        self.organizer_name = organizer_name
        self.login = login
        self.secret_key = secret_key
