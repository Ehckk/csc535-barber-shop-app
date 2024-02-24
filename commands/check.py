from database import Database, format_table


def show_tables(db: Database):
    db.show()
    for name, schema in db.schemas.items():
        format_table(name, schema)