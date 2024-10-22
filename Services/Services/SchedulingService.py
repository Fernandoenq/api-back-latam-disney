from Application.Models.Request.ReschedulingRequestModel import ReschedulingRequestModel
from Domain.Entities.Scheduling import Scheduling
from Domain.Enums.SchedulingStatus import SchedulingStatus
import pandas as pd
from datetime import datetime
from typing import List


class SchedulingService:
    @staticmethod
    def get_schedules_by_id(cursor, scheduling_id: int) -> pd.DataFrame:
        cursor.execute("""Select s.PersonId, s.OrganizerId
                            From Scheduling s 
                            Where s.SchedulingId = %s""", (scheduling_id,))
        scheduling_loaded = cursor.fetchall()

        scheduling = Scheduling()
        return pd.DataFrame(scheduling_loaded, columns=[scheduling.person_id, scheduling.organizer_id])

    @staticmethod
    def get_schedules_by_cpf(cursor, cpf: str) -> pd.DataFrame:
        now = datetime.now()
        today = now.date()

        cursor.execute("""
            SELECT s.SchedulingId, t.TurnId, t.TurnTime, s.SchedulingStatus 
            FROM Scheduling s
            JOIN Person p ON p.PersonId = s.PersonId
            JOIN Turn t ON t.TurnId = s.TurnId
            WHERE p.Cpf = %s
            AND t.TurnTime > %s
            AND DATE(t.TurnTime) = %s
            ORDER BY t.TurnTime ASC
        """, (cpf, now, today))

        scheduling_loaded = cursor.fetchall()

        return SchedulingService._to_scheduling_df(scheduling_loaded)

    @staticmethod
    def get_schedules(cursor) -> pd.DataFrame:
        now = datetime.now()
        today = now.date()

        cursor.execute("""
                        SELECT s.SchedulingId, t.TurnId, t.TurnTime, s.SchedulingStatus 
                        FROM Scheduling s
                        JOIN Turn t on t.TurnId = s.TurnId
                        WHERE t.TurnTime > %s
                        AND DATE(t.TurnTime) = %s
                        ORDER BY t.TurnTime ASC
                        """, (now, today))
        scheduling_loaded = cursor.fetchall()

        return SchedulingService._to_scheduling_df(scheduling_loaded)

    @staticmethod
    def get_all_schedules(cursor) -> pd.DataFrame:
        cursor.execute("""SELECT p.PersonName, p.Cpf, t.TurnTime, c.ChairName, s.SchedulingStatus FROM Scheduling s
                        JOIN Person p on p.PersonId = s.PersonId
                        JOIN Room r on r.RoomId = s.RoomId
                        JOIN Chair c on c.ChairId = s.ChairId
                        JOIN Turn t on t.TurnId = s.TurnId
                        ORDER BY t.TurnTime DESC""")
        scheduling_loaded = cursor.fetchall()

        scheduling = Scheduling()
        scheduling_df = pd.DataFrame(scheduling_loaded, columns=[scheduling.person.person_name, scheduling.person.cpf,
                                                                 scheduling.turn.turn_time, scheduling.chair.chair_name,
                                                                 scheduling.scheduling_status])

        scheduling_df[scheduling.turn.turn_time] = pd.to_datetime(scheduling_df[scheduling.turn.turn_time]).dt.strftime(
            '%d/%m %H:%M')

        return scheduling_df

    @staticmethod
    def to_schedule(cursor, person_id: int, organizer_id: int, scheduling_id: int) -> bool:
        cursor.execute("""Update Scheduling set PersonId = %s, OrganizerId = %s, SchedulingStatus = %s  
                        WHERE SchedulingId = %s""",
                       (person_id, organizer_id, SchedulingStatus.busy.value, scheduling_id))

        return cursor.rowcount > 0

    @staticmethod
    def to_reschedule(cursor, rescheduling_request: ReschedulingRequestModel) -> bool:
        scheduling_df = SchedulingService.get_schedules_by_id(cursor, rescheduling_request.old_scheduling_id)

        cursor.execute(
            """Update Scheduling set PersonId = null, OrganizerId = null, SchedulingStatus = %s 
            WHERE SchedulingId = %s""", (SchedulingStatus.available.value, rescheduling_request.old_scheduling_id,))

        if cursor.rowcount <= 0:
            return False

        scheduling = Scheduling()
        return SchedulingService.to_schedule(cursor, int(scheduling_df[scheduling.person_id][0]),
                                             int(scheduling_df[scheduling.organizer_id][0]),
                                             rescheduling_request.new_scheduling_id)

    @staticmethod
    def confirm_presence(cursor, scheduling_id: int) -> bool:
        cursor.execute(
            """Update Scheduling set SchedulingStatus = %s WHERE SchedulingId = %s""",
            (SchedulingStatus.confirmed.value, scheduling_id,))

        return cursor.rowcount > 0

    @staticmethod
    def insert_schedules(cursor, schedules: List) -> bool:
        for schedule in schedules:
            insert_turn_query = "INSERT INTO Turn (TurnTime) VALUES (%s)"
            cursor.execute(insert_turn_query, (schedule,))

            turn_id = cursor.lastrowid

            insert_scheduling_query = """
            INSERT INTO Scheduling (PersonId, OrganizerId, TurnId, RoomId, ChairId, SchedulingStatus)
            VALUES (NULL, NULL, %s, 1, %s, %s)
            """
            cursor.execute(insert_scheduling_query, (turn_id, 1, SchedulingStatus.available.value))
            cursor.execute(insert_scheduling_query, (turn_id, 2, SchedulingStatus.available.value))

        return cursor.rowcount > 0

    @staticmethod
    def _to_scheduling_df(scheduling_loaded) -> pd.DataFrame:
        scheduling = Scheduling()

        scheduling_df = pd.DataFrame(scheduling_loaded, columns=[scheduling.scheduling_id, scheduling.turn_id,
                                                                 scheduling.turn.turn_time,
                                                                 scheduling.scheduling_status])

        scheduling_df[scheduling.turn.turn_time] = pd.to_datetime(scheduling_df[scheduling.turn.turn_time]).dt.strftime(
            '%Y-%m-%d %H:%M:%S')

        return scheduling_df
