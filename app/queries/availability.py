from datetime import date
from ..utils.date import date_window
from .. import db


def list_barber_unavailible_ranges(barber_id: int, current: date, units: str):
    start_date, end_date = date_window(current, units)
    query = """
        SELECT start_date, end_date 
        FROM csc535_barber.unavailable
        WHERE barber_id = %(barber_id)s
        AND end_date IS NOT NULL
        AND (
            start_date BETWEEN %(start_date)s AND %(end_date)s OR
            end_date BETWEEN %(start_date)s AND %(end_date)s
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


def list_barber_unavailible_dates(barber_id: int, current: date, units: str):
    start_date, end_date = date_window(current, units)
    query = """
        SELECT start_date, end_date 
        FROM csc535_barber.unavailable
        WHERE barber_id = %(barber_id)s
        AND end_date IS NULL
        AND start_date BETWEEN %(start_date)s AND %(end_date)s
    """
    results = db.execute(query, {
        "barber_id": int(barber_id), 
        "start_date": str(start_date), 
        "end_date": str(end_date), 
    })
    if not results:
        return []
    return results


def get_overlapping_ranges(barber_id: int, start_date: date, end_date: date):
    query = """
        SELECT 
            MIN(unavailable_id) AS unavailable_id,
            MIN(start_date) AS min_start,
            MAX(end_date) AS max_end
        FROM csc535_barber.unavailable
        WHERE barber_id = %(barber_id)s 
        AND (
            start_date BETWEEN %(start_date)s AND %(end_date)s 
            OR end_date BETWEEN %(start_date)s AND %(end_date)s
        )
    """
    results = db.execute(query, {
        "barber_id": int(barber_id), 
        "start_date": str(start_date), 
        "end_date": str(end_date), 
    })
    if results:
        return results[0]
    return []


def delete_unavailable_ranges(new_id: int, barber_id: int, start_date: date, end_date: date):
    query = """
        DELETE FROM csc535_barber.unavailable
        WHERE barber_id = %(barber_id)s 
        AND NOT unavailable_id = %(new_id)s 
        AND (
            start_date BETWEEN %(start_date)s AND %(end_date)s 
            OR end_date BETWEEN %(start_date)s AND %(end_date)s
        )
    """
    db.execute(query, {
        "new_id": int(new_id),
        "barber_id": int(barber_id),
        "start_date": str(start_date),
        "end_date": str(end_date) 
    })
    db.commit()


def update_unavailable_range(unavailable_id: int, start_date: str, end_date: str):
    query = """
        UPDATE csc535_barber.unavailable 
        SET start_date = %(start_date)s,
            end_date = %(end_date)s
        WHERE unavailable_id = %(unavailable_id)s;
    """
    db.execute(query, {
        "unavailable_id": unavailable_id,
        "start_date": start_date,
        "end_date": end_date
    })
    db.commit()


def create_unavailable_range(barber_id: int, start_date: date, end_date: date | None):
    if end_date:
        result = get_overlapping_ranges(barber_id, start_date, end_date)
        if result:
            new_id = result["unavailable_id"]
            new_start = min(str(start_date), str(result["min_start"]))
            new_end = max(str(end_date), str(result["max_end"]))
            update_unavailable_range(new_id, new_start, new_end)
            delete_unavailable_ranges(new_id, barber_id, start_date, end_date)
            return 
    
    query = """
        INSERT INTO csc535_barber.unavailable VALUES 
            (DEFAULT, %(barber_id)s, %(start_date)s, %(end_date)s, DEFAULT);
    """
    db.execute(query, {
        "barber_id": int(barber_id),
        "start_date": str(start_date),
        "end_date": None if end_date is None else str(end_date) 
    })
    db.commit()
    

def has_unavailability_for_date(barber_id: int, target_date: date):
    query = """
        SELECT * FROM csc535_barber.unavailable
        WHERE barber_id = %(barber_id)s
        AND start_date = %(target_date)s
        AND end_date IS NULL
        UNION
        SELECT * FROM csc535_barber.unavailable
        WHERE barber_id = %(barber_id)s
        AND %(target_date)s BETWEEN start_date AND end_date
        AND end_date IS NOT NULL
    """
    results = db.execute(query, {
        "barber_id": barber_id,
        "target_date": target_date
    })
    return bool(results)


def has_unavailability_for_range(barber_id: int, start_date: date, end_date: date):
    query = """
        SELECT * FROM csc535_barber.unavailable
        WHERE barber_id = %(barber_id)s
        AND end_date IS NOT NULL
        AND %(start_date)s BETWEEN start_date AND end_date
        AND %(end_date)s BETWEEN start_date AND end_date
    """
    results = db.execute(query, {
        "barber_id": barber_id,
        "start_date": start_date,
        "end_date": end_date
    })
    return bool(results)
    