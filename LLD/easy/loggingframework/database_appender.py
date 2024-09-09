import psycopg2
from log_message import LogMessage
from log_appender import LogAppender


class DatabaseAppender(LogAppender):
    def __init__(self, db_url: str, username: str, password: str):
        self.db_url = db_url
        self.username = username
        self.password = password

    def append(self, log_message: LogMessage):
        try:
            connection = psycopg2.connect(self.db_url, self.username, self.password)
            cursor = connection.cursor()
            cursor.execute(
                "INSER INTO LOGS (level, message, timestamp) VALUES (%s, %s, %s)",
                (
                    log_message.get_level().name,
                    log_message.get_message(),
                    log_message.get_timestamp(),
                ),
            )
            connection.commit()
            cursor.close()
            connection.close()
        except psycopg2.Error as e:
            print(f"Error {e}")
