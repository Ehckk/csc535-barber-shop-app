from pymysql import Connection
from pymysql.cursors import DictCursor 


def connect_db(config):
    try:
        print("Connecting to database...")
        name = config["MYSQL_DB"]
        connection = Connection(
            host=config["MYSQL_IP"],
            port=int(config["MYSQL_PORT"]),
            user=config["MYSQL_USER"],
            password=config["MYSQL_PASSWORD"],
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=True,
            init_command=f"CREATE DATABASE IF NOT EXISTS {name};",
            database=name
        )
    except KeyError as key:
        message = f"Unable to find required environment variable {key} in \'.flaskenv\'. Does it exist?"
        raise KeyError(message)
    connection.select_db(name)
    print(f"Connected to database \'{name}\'")
    return connection
