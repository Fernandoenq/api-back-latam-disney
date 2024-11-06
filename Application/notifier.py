import schedule
import time
import boto3
import json
from datetime import datetime, timedelta
from Services.Services.ConnectionService import ConnectionService
from Services.Services.SchedulingService import SchedulingService
from Domain.Entities.Scheduling import Scheduling
from Application.Configuration import Configuration
import threading
from Services.Services.SqsService import SqsService

lock = threading.Lock()


def to_format_name(name):
    part_name = name.strip().split()

    if len(part_name) == 1:
        return part_name[0].capitalize()

    return f"{part_name[0].capitalize()} {part_name[-1].capitalize()}"


def notify():
    with lock:
        connection = None
        cursor = None
        try:
            connection = ConnectionService.open_connection()
            connection.start_transaction()
            cursor = connection.cursor()

            now = datetime.now()
            advance_date = now + timedelta(minutes=20)

            notifiable_schedules_df = SchedulingService().get_notifiable_schedules(cursor, advance_date, now)
            if notifiable_schedules_df.empty:
                print(f"[Notificador] Nenhuma notificação: {datetime.now()}")
                return

            schedule_df = Scheduling()
            for index, row in notifiable_schedules_df.iterrows():
                name = to_format_name(row[schedule_df.person.person_name])
                phone = row[schedule_df.person.phone]

                message_sqs = {
                    "origin": 1,
                    "phone": phone,
                    "message": (f"Atenção!\n\nSeu embarque começa em 15 minutos. Dirija-se ao stand da LATAM e "
                                f"prepare-se para decolar rumo aos Destinos Encantados")
                }

                response = SqsService().notify(message_sqs, name, phone)

                if response:
                    SchedulingService().to_confirm_notification(cursor, int(row[schedule_df.scheduling_id]))
                else:
                    continue

            connection.commit()
            print(f"[Notificador] Última notificação: {datetime.now()}")

        except Exception as e:
            if connection is not None and connection.is_connected():
                connection.rollback()
            print(e)
            return
        finally:
            if connection is not None and cursor is not None and connection.is_connected():
                ConnectionService.close_connection(cursor, connection)
            return


schedule.every(2).minutes.do(notify)

while True:
    schedule.run_pending()
    time.sleep(1)
