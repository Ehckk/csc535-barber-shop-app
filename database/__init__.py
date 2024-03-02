from .config import app_config
from .connect import connect_db


class Database:
    def __init__(self, config) -> None:
        self.connection = connect_db(config)

    def execute(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor
        

db = Database(app_config)
