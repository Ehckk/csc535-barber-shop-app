from datetime import date
from config import app_config
from data.db import Database


def test_db():
    db = Database(app_config)
    res = db.execute("SELECT CURDATE() AS `today`").fetchone()
    assert res["today"] == date.today()
