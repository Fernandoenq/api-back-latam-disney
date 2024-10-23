import pandas as pd
from Domain.Entities.Person import Person
from Domain.Entities.Organizer import Organizer
from Domain.Entities.Turn import Turn
from Domain.Entities.Room import Room
from Domain.Entities.Chair import Chair


class Scheduling:
    def __init__(self):
        self.scheduling_id = 'SchedulingId'
        self.person_id = 'PersonId'
        self.scheduling_date = 'SchedulingDate'
        self.confirmation_date = 'ConfirmationDate'
        self.organizer_id = 'OrganizerId'
        self.turn_id = 'TurnId'
        self.room_id = 'RoomId'
        self.chair_id = 'ChairId'
        self.scheduling_status = 'SchedulingStatus'
        self.chair = Chair()
        self.person = Person()
        self.room = Room()
        self.organizer = Organizer()
        self.turn = Turn()

        self.scheduling_df = pd.DataFrame(columns=[self.scheduling_id, self.person_id, self.scheduling_date,
                                                   self.confirmation_date, self.organizer_id, self.turn_id,
                                                   self.room_id, self.chair_id, self.scheduling_status])
