from datetime import date
from database import db


def test_db():
    res = db.execute("SELECT CURDATE() AS `today`").fetchone()
    assert res["today"] == date.today()
