from datetime import date
from database import db


def test_db():
    res = db.execute("SELECT CURDATE() AS `today`")
    assert res[0]["today"] == date.today()

