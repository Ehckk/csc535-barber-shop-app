from database import db


def test_retrieve_services():
    query = """
        SELECT * 
        FROM csc535_barber.service
        WHERE `name` = %(name)s    
    """
    res = db.execute(query, {'name': 'Beard Trim'})
    assert len(res) == 1
    res = db.execute(query, {'name': '326730223598020368724r38723'})
    assert len(res) == 0