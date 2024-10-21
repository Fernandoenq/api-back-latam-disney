import schedule
import time
from datetime import datetime
from Services.Services.ConnectionService import ConnectionService
from Application.Constants import Constants
import threading
import pywhatkit as kit

lock = threading.Lock()


def notify():
    with lock:
        connection = None
        cursor = None
        try:
            connection = ConnectionService.open_connection()
            connection.start_transaction()
            cursor = connection.cursor()
            current_date = datetime.now()

            numero_destino = "+5511991225937"
            mensagem = "Olá, estou testando o envio automático de mensagens no WhatsApp!"
            agora = datetime.now()
            hora_envio = agora.hour
            minuto_envio = agora.minute + 1  # Adicionando 1 minuto para dar tempo de abrir o WhatsApp

            # Enviar a mensagem
            kit.sendwhatmsg(numero_destino, mensagem, hora_envio, minuto_envio)

            # Enviar a mensagem
            kit.sendwhatmsg(numero_destino, mensagem, hora_envio, minuto_envio)

            connection.commit()
            print(f"[Notificador]: Última notificaçaõ: {datetime.now()}")

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
