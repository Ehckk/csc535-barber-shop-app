from ... import db


def login_user(email, password):
    query = """
        SELECT * FROM csc535_barber.`user`
        WHERE `email` = %(email)s 
        AND `password` = %(password)s
    """
    cursor = db.execute(query, {"email": email, "password": password})
    return cursor.fetchone()
