from Domain.Entities.Organizer import Organizer


class OrganizerLoginRequestModel:
    def __init__(self, login_request):
        organizer = Organizer()
        self.login = login_request[organizer.login]
        self.secret_key = login_request[organizer.secret_key]
        """
        self.service_type = login_request['ServiceType']
        self.service_id = login_request['ServiceId']
        """
