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

lock = threading.Lock()
sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=Configuration.aws_access_key_id,
    aws_secret_access_key=Configuration.aws_secret_access_key,
    region_name=Configuration.region_name
)


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
                return

            schedule_df = Scheduling()
            for index, row in notifiable_schedules_df.iterrows():
                name = to_format_name(row[schedule_df.person.person_name])
                turn_time = row[schedule_df.turn.turn_time]
                phone = row[schedule_df.person.phone]

                message_sqs = {
                    "origin": 1,
                    "phone": phone,
                    "message": (f"Olá, {name}! Sua sessão começará às {turn_time.strftime('%H:%M')}. "
                                f"Prepare-se que já iremos decolar!")
                }

                try:
                    response = sqs_client.send_message(
                        QueueUrl=Configuration.sqs_queue_url,
                        MessageBody=json.dumps(message_sqs)
                    )

                    if response.get('MessageId'):
                        print(f"Mensagem enviada com sucesso para {name} / {phone}. "
                              f"ID da mensagem: {response['MessageId']}")

                        SchedulingService().to_confirm_notification(cursor, int(row[schedule_df.scheduling_id]))
                    else:
                        print(f"Falha ao enviar mensagem para {name} / {phone}.")
                        continue

                except Exception as e:
                    print(f"Erro ao enviar mensagem para {name} / {phone}: {e}")
                    continue

            connection.commit()
            print(f"[Notificador]: Última notificação: {datetime.now()}")

        except Exception as e:
            if connection is not None and connection.is_connected():
                connection.rollback()
            print(e)
            return
        finally:
            if connection is not None and cursor is not None and connection.is_connected():
                ConnectionService.close_connection(cursor, connection)
            return


schedule.every(1).seconds.do(notify)

while True:
    schedule.run_pending()
    time.sleep(1)
