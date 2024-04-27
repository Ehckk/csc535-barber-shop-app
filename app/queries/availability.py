from datetime import date
from ..utils.date import date_window
from .. import db


def list_barber_unavailible_dates(barber_id: int, current: date, units: str):
    start_date, end_date = date_window(current, units)
    query = """
        SELECT start_date, end_date 
        FROM csc535_barber.unavailable
        WHERE barber_id = %(barber_id)s
        AND (
            (
                start_date BETWEEN %(start_date)s AND %(end_date)s OR
                end_date BETWEEN %(start_date)s AND %(end_date)s
            ) 
            OR %(end_date)s IS NULL and start_date = %(start_date)s
        )
    """
    results = db.execute(query, {
        "barber_id": int(barber_id), 
        "start_date": str(start_date), 
        "end_date": str(end_date),
    })
    if not results:
        return []
    return results