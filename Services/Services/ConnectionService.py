import mysql.connector
from Application.Configuration import Configuration


class ConnectionService:
    def __init__(self):
        pass

    @staticmethod
    def open_connection():
        connection = mysql.connector.connect(
            host=Configuration.host,
            user=Configuration.user,
            password=Configuration.password,
            database=Configuration.database,
        )

        return connection

    @staticmethod
    def close_connection(cursor, connection):
        cursor.close()
        connection.close()
