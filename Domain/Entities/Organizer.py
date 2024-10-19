import pandas as pd


class Organizer:
    def __init__(self):
        self.organizer_id = 'OrganizerId'
        self.organizer_name = 'OrganizerName'
        self.login = 'Login'
        self.secret_key = 'SecretKey'

        self.person_df = pd.DataFrame(columns=[self.organizer_id, self.organizer_name, self.login, self.secret_key])
