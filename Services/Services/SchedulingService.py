from Application.Models.Request.ReschedulingRequestModel import ReschedulingRequestModel
from Domain.Entities.Scheduling import Scheduling
from Domain.Enums.SchedulingStatus import SchedulingStatus
import pandas as pd
from datetime import datetime, timedelta
from typing import List


class SchedulingService:
    @staticmethod
    def get_schedules_by_id(cursor, scheduling_id: int) -> pd.DataFrame:
        cursor.execute("""Select s.PersonId, s.OrganizerId, s.SchedulingStatus
                            From Scheduling s 
                            Where s.SchedulingId = %s""", (scheduling_id,))
        scheduling_loaded = cursor.fetchall()

        scheduling = Scheduling()
        return pd.DataFrame(scheduling_loaded, columns=[scheduling.person_id, scheduling.organizer_id,
                                                        scheduling.scheduling_status])

    @staticmethod
    def get_turns_by_schedule_id(cursor, scheduling_id: int) -> pd.DataFrame:
        cursor.execute("""
                        SELECT PersonId, TurnId
                        FROM Scheduling
                        WHERE TurnId = (
                            SELECT TurnId 
                            FROM Scheduling
                            WHERE SchedulingId = %s
                        );""", (scheduling_id,))
        scheduling_loaded = cursor.fetchall()

        scheduling = Scheduling()
        return pd.DataFrame(scheduling_loaded, columns=[scheduling.person_id, scheduling.turn_id])

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
            AND s.SchedulingStatus = %s
            AND t.TurnTime > %s
            AND DATE(t.TurnTime) = %s
            ORDER BY t.TurnTime ASC
        """, (cpf, SchedulingStatus.busy.value, now, today))

        scheduling_loaded = cursor.fetchall()

        return SchedulingService._to_scheduling_df(scheduling_loaded)

    @staticmethod
    def get_schedules(cursor) -> pd.DataFrame:
        now = datetime.now() + timedelta(minutes=1)
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
        cursor.execute("""SELECT p.PersonName, p.Cpf, s.SchedulingDate, t.TurnTime, c.ChairName, s.SchedulingStatus 
                        FROM Scheduling s
                        LEFT JOIN Person p on p.PersonId = s.PersonId
                        JOIN Room r on r.RoomId = s.RoomId
                        JOIN Chair c on c.ChairId = s.ChairId
                        JOIN Turn t on t.TurnId = s.TurnId
                        ORDER BY t.TurnTime ASC""")
        scheduling_loaded = cursor.fetchall()

        scheduling = Scheduling()
        scheduling_df = pd.DataFrame(scheduling_loaded, columns=[
            scheduling.person.person_name,
            scheduling.person.cpf,
            scheduling.scheduling_date,
            scheduling.turn.turn_time,
            scheduling.chair.chair_name,
            scheduling.scheduling_status
        ])

        scheduling_df[scheduling.turn.turn_time] = pd.to_datetime(
            scheduling_df[scheduling.turn.turn_time], errors='coerce'
        ).dt.strftime('%d/%m %H:%M')

        scheduling_df[scheduling.scheduling_date] = pd.to_datetime(
            scheduling_df[scheduling.scheduling_date], errors='coerce'
        ).dt.strftime('%d/%m %H:%M')

        scheduling_df = scheduling_df.where(pd.notnull(scheduling_df), None)

        return scheduling_df

    @staticmethod
    def get_notifiable_schedules(cursor, advance_date: datetime, now: datetime) -> pd.DataFrame:
        cursor.execute("""
                        SELECT p.PersonName, p.Phone, t.TurnTime, s.SchedulingId FROM `Scheduling` s 
                        JOIN Person p on p.PersonId = s.PersonId
                        JOIN Turn t on t.TurnId = s.TurnId
                        WHERE s.SchedulingStatus = %s
                        AND t.TurnTime >= %s
                        AND t.TurnTime <= %s
                        And s.IsNotified = 0
                        """, (SchedulingStatus.busy.value, now, advance_date))
        scheduling_loaded = cursor.fetchall()

        scheduling = Scheduling()
        return pd.DataFrame(scheduling_loaded, columns=[scheduling.person.person_name, scheduling.person.phone,
                                                        scheduling.turn.turn_time, scheduling.scheduling_id])

    @staticmethod
    def get_person_to_confirm(cursor, scheduling_id: int) -> pd.DataFrame:
        cursor.execute("""
                            SELECT p.PersonName, p.Phone, t.TurnTime FROM Scheduling s 
                            JOIN Person p on p.PersonId = s.PersonId
                            JOIN Turn t on t.TurnId = s.TurnId
                            WHERE s.SchedulingId= %s
                            """, (scheduling_id,))
        scheduling_loaded = cursor.fetchall()

        scheduling = Scheduling()
        return pd.DataFrame(scheduling_loaded, columns=[scheduling.person.person_name, scheduling.person.phone,
                                                        scheduling.turn.turn_time])

    @staticmethod
    def to_confirm_notification(cursor, scheduling_id: int) -> bool:
        cursor.execute("""Update Scheduling set IsNotified = 1 WHERE SchedulingId = %s """, (scheduling_id,))
        return cursor.rowcount > 0

    @staticmethod
    def to_schedule(cursor, person_id: int, organizer_id: int, scheduling_id: int) -> bool:
        cursor.execute("""Update Scheduling set PersonId = %s, OrganizerId = %s, SchedulingStatus = %s,
                        SchedulingDate = %s
                        WHERE SchedulingId = %s""",
                       (person_id, organizer_id, SchedulingStatus.busy.value, datetime.now(), scheduling_id))

        return cursor.rowcount > 0

    @staticmethod
    def to_reschedule(cursor, rescheduling_request: ReschedulingRequestModel) -> bool:
        scheduling_df = SchedulingService.get_schedules_by_id(cursor, rescheduling_request.old_scheduling_id)

        cursor.execute(
            """Update Scheduling set PersonId = null, OrganizerId = null, SchedulingDate = null, SchedulingStatus = %s 
            IsNotified = 0 WHERE SchedulingId = %s""",
            (SchedulingStatus.available.value, rescheduling_request.old_scheduling_id,))

        if cursor.rowcount <= 0:
            return False

        scheduling = Scheduling()
        return SchedulingService.to_schedule(cursor, int(scheduling_df[scheduling.person_id][0]),
                                             int(scheduling_df[scheduling.organizer_id][0]),
                                             rescheduling_request.new_scheduling_id)

    @staticmethod
    def confirm_presence(cursor, scheduling_id: int) -> bool:
        cursor.execute(
            """Update Scheduling set SchedulingStatus = %s, ConfirmationDate = %s WHERE SchedulingId = %s""",
            (SchedulingStatus.confirmed.value, datetime.now(), scheduling_id,))

        return cursor.rowcount > 0

    @staticmethod
    def cancel_schedule(cursor, scheduling_id: int) -> bool:
        cursor.execute(
            """Update Scheduling set PersonId = null, OrganizerId = null, SchedulingDate = null, SchedulingStatus = %s, 
            IsNotified = 0, ConfirmationDate = null 
            WHERE SchedulingId = %s""", (SchedulingStatus.available.value, scheduling_id,))

        return cursor.rowcount >= 0

    @staticmethod
    def insert_schedules(cursor, schedules: List) -> bool:
        for schedule in schedules:
            insert_turn_query = "INSERT INTO Turn (TurnTime) VALUES (%s)"
            cursor.execute(insert_turn_query, (schedule,))

            turn_id = cursor.lastrowid

            insert_scheduling_query = """
            INSERT INTO Scheduling (PersonId, SchedulingDate, ConfirmationDate, OrganizerId, TurnId, RoomId, ChairId, 
            SchedulingStatus, IsNotified) VALUES (NULL, NULL, NULL, NULL, %s, 1, %s, %s, 0)
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
