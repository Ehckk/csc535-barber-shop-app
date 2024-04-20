from .config import app_config
from .connect import connect_db


class Database:
    def __init__(self, config) -> None:
        self.connection = connect_db(config)

    def execute(self, sql, params=None):
        results = []
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            result_set = cursor.fetchall()
            if result_set is None:
                return None
            for result in result_set:
                results.append(result)
        return results

        
    def commit(self):
        self.connection.commit()
        

db = Database(app_config)
