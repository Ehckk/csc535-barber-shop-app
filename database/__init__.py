from .config import app_config
from .connect import connect_db
from .table import format_table


class Database:
    def __init__(self, config) -> None:
        self.connection = connect_db(config)
        self.update_schemas()

    def execute(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor

    def fmt_table(self, name, schema):
        return

    def update_schemas(self):
        schemas = {}
        with self.connection.cursor() as cursor:
            cursor.execute('SHOW TABLES;')
            tables = cursor.fetchall()
            for table in tables:
                table_name, = table.values()
                cursor.execute(f'DESCRIBE {table_name};')
                schemas[table_name] = cursor.fetchall()
        self.schemas = schemas

    def show(self):
        print(self.schemas)
        return self.schemas
        

db = Database(app_config)
