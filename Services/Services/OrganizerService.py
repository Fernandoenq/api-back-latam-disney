from typing import List
import pandas as pd
from Domain.Entities.Organizer import Organizer
from Application.Models.Request.OrganizerRequestModel import OrganizerRequestModel
from Application.Models.Request.OrganizerLoginRequestModel import OrganizerLoginRequestModel


class OrganizerService:
    @staticmethod
    def get_organizer(cursor) -> pd.DataFrame:
        cursor.execute("Select OrganizerId, OrganizerName From Organizer")
        organizers = cursor.fetchall()

        organizer = Organizer()
        return pd.DataFrame(organizers, columns=[organizer.organizer_id, organizer.organizer_name])

    @staticmethod
    def get_organizer_by_login(login: str, cursor) -> pd.DataFrame:
        cursor.execute("Select OrganizerId, OrganizerName From Organizer Where Login = %s", (login,))
        organizers = cursor.fetchall()

        organizer = Organizer()
        return pd.DataFrame(organizers, columns=[organizer.organizer_id, organizer.organizer_name])

    @staticmethod
    def get_organizer_by_id(organizer_id: str, cursor) -> pd.DataFrame:
        cursor.execute("Select OrganizerId, OrganizerName From Organizer Where OrganizerId = %s", (organizer_id,))
        organizers = cursor.fetchall()

        organizer = Organizer()
        return pd.DataFrame(organizers, columns=[organizer.organizer_id, organizer.organizer_name])

    @staticmethod
    def update_organizer(organizers_request: List[OrganizerRequestModel], cursor) -> pd.DataFrame:
        for organizer_request in organizers_request:
            cursor.execute("""UPDATE Organizer SET (OrganizerName = %s, Login = %s, SecretKey = %s) 
                                        WHERE OrganizerId = %s""", (organizer_request.organizer_name,
                                                                    organizer_request.login,
                                                                    organizer_request.secret_key,
                                                                    organizer_request.organizer_id))

        return OrganizerService.get_organizer(cursor)

    @staticmethod
    def create_organizer(organizers_request: List[OrganizerRequestModel], cursor) -> pd.DataFrame:
        for organizer_request in organizers_request:
            cursor.execute("INSERT INTO Organizer (OrganizerName, Login, SecretKey) VALUES (%s, %s, %s)",
                           (organizer_request.organizer_name, organizer_request.login, organizer_request.secret_key))

        return OrganizerService.get_organizer(cursor)

    @staticmethod
    def delete_organizer(organizers_request: List[OrganizerRequestModel], cursor) -> pd.DataFrame:
        for organizer_request in organizers_request:
            cursor.execute("DELETE FROM Organizer WHERE OrganizerId = %s", (organizer_request.organizer_id,))

        return OrganizerService.get_organizer(cursor)

    @staticmethod
    def login(login_request: OrganizerLoginRequestModel, cursor) -> pd.DataFrame:
        cursor.execute("Select OrganizerId, OrganizerName from Organizer Where Login = %s And SecretKey = %s",
                       (login_request.login, login_request.secret_key))
        loaded_organizer = cursor.fetchall()

        organizer = Organizer()
        organizer_df = pd.DataFrame(loaded_organizer, columns=[organizer.organizer_id,
                                                               organizer.organizer_name])

        if organizer_df.empty:
            return organizer_df

        return organizer_df
