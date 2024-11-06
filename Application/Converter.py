from datetime import datetime
import pandas as pd
from Services.Services.SchedulingService import SchedulingService
from Services.Services.ConnectionService import ConnectionService
from mysql.connector import Error

connection = ConnectionService.open_connection()
cursor = connection.cursor()
connection.start_transaction()

try:
    file_path = r'C:\Users\Juliano César\Documents\GitHub\api-back-latam-disney\Repositories\Excel/Horarios.csv'
    df = pd.read_csv(file_path, sep=';')

    schedules = []
    for index, row in df.iterrows():
        day = row['Data']
        time = row['Horario']
        schedule = datetime.strptime(f'2024-11-{int(day)} {time}', '%Y-%m-%d %Hh%M')
        schedules.append(schedule)

    SchedulingService.insert_schedules(cursor, schedules)
    connection.commit()
    print('Sucesso')

except Error as e:
    if connection.is_connected():
        connection.rollback()
    print(f"Erro de banco de dados: {e}")
finally:
    if connection.is_connected():
        ConnectionService.close_connection(cursor, connection)
