from pymysql import Connection
from pymysql.cursors import DictCursor 


def connect(config):
    try:
        print("Connecting to database...")
        connection = Connection(
            host=config["MYSQL_IP"],
            port=int(config["MYSQL_PORT"]),
            user=config["MYSQL_USER"],
            password=config["MYSQL_PASSWORD"],
            database=config["MYSQL_DB"],
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=True
        )
    except KeyError as key:
        message = f"Unable to find required environment variable {key} in \'.flaskenv\'. Does it exist?"
        raise KeyError(message)
    
    name = connection.db.decode("ascii")
    print(f"Connected to database \'{name}\'")
    return name, connection
