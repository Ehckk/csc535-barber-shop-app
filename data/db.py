from .connect import connect


class Database:
    def __init__(self, config) -> None:
        name, connection = connect(config)
        self.name = name
        self.connection = connection

    def execute(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor