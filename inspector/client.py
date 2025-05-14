from config import database_path

from config import cursor, connect
from collections import defaultdict
import hashlib
from datetime import datetime, timedelta

def hash(data):
    sha256_hash = hashlib.new('sha256')
    sha256_hash.update(data.encode())
    return sha256_hash.hexdigest()

from random import randint

def driver_check(list_):
    fio, seria, nomer, vu, date = list_
    fio = fio.split(" ")
    fio.append(" ")
    lastname, name, fathername = fio[:3]

    lastname, name, fathername = hash(lastname), hash(name), hash(fathername)
    passport = seria + " " + nomer

    driver_id = cursor.execute(
        "SELECT id FROM DRIVERS WHERE lastname = ? AND name = ? AND fathername = ? AND passport = ? and birth_date = ?",
        (lastname, name, fathername, passport, date)
    ).fetchone()

    if driver_id:
        return True
    return False


def gen_vu(numer):
    
    num = [randint(0, 9) for _ in range(10)]
    s = ''.join(map(str, num))
    vu = f"{s[:4]} {s[4:]}"

    vu_id = cursor.execute("SELECT id FROM VU WHERE numer = ?", (numer, )).fetchone()

    if vu_id is None:
        return False

    vu_id = vu_id[0]

    end_date = cursor.execute("SELECT end_date FROM VU WHERE id = ?", (vu_id, )).fetchone()[0]
    
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    today = datetime.now().date()

    end_date = today + timedelta(days=365*10)
    today = today.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    cursor.execute("""
    UPDATE VU SET numer = ?, start_date = ?, end_date = ? WHERE id = ?
""", (vu, today, end_date, vu_id, ))
    connect.commit()
    return True, vu, end_date

def get_driver_id(lastname, name, fathername):
    driver_id = cursor.execute("SELECT id FROM DRIVERS WHERE lastname = ? AND name = ? AND fathername = ?", (lastname, name, fathername, )).fetchone()[0]
    return driver_id

def get_driver_id_vu(list_):
    lastname, name, fathername, numer = list_
    driver_id = cursor.execute("SELECT d.id FROM DRIVERS d JOIN VU vu ON vu.id = driver_id WHERE lastname = ? AND name = ? AND fathername = ? AND vu.numer = ?", (lastname, name, fathername, numer, )).fetchone()[0]
    return driver_id

def del_fine(list_):
    fio, numer, fine_num = list_

    if check_pay_fine(fine_num):
        return True, f"Штраф №{fine_num} уже был оплачен"

    fio = fio.split(" ")
    fio.append(" ")
    lastname, name, fathername = fio[:3]
    lastname, name, fathername = hash(lastname), hash(name), hash(fathername)
    dr_id = get_driver_id_vu([lastname, name, fathername, numer])
    if dr_id:
        cursor.execute("""
            UPDATE FINES SET status = ? WHERE uid = ? and driver_id = ?;
        """, ("Оплачен", fine_num, get_driver_id(lastname, name, fathername), ))
        connect.commit()
        return True, f"Штраф №{fine_num} был оплачен"
    return False, "такого не было"

def check_pay_fine(nomer):
    fine = cursor.execute("SELECT * FROM FINES WHERE uid = ? AND status = 'Не оплачен'", (nomer, )).fetchone()
    if fine:
        return False
    return True

def check_fine(nomer):
    fine = cursor.execute("SELECT * FROM FINES WHERE uid = ?", (nomer, )).fetchone()
    if fine:
        return True
    return False

def add_fine(list_):
    fio, numer, nomer, reason, summa = list_
    fio = fio.split(" ")
    fio.append(" ")
    lastname, name, fathername = fio[:3]
    lastname, name, fathername = hash(lastname), hash(name), hash(fathername)
    dr_id = get_driver_id_vu([lastname, name, fathername, numer])
    today = datetime.now().strftime('%Y-%m-%d')
    fine = check_fine(nomer)
    if dr_id and not fine:
        fine = (
            dr_id, nomer, reason, summa, today, "Не оплачен",
        )

        cursor.execute(
            f"""INSERT INTO `FINES` (driver_id, uid, reason, summa, date, status) VALUES (?, ?, ?, ?, ?, ?)""", fine
        )
        connect.commit()
        return True, f"Штраф №{nomer} был зарегистрирован в системе"
    return True, f"Штраф №{nomer} уже зарегистрирован в системе" 

def check_transport(list_):
    ts = cursor.execute("SELECT driver_id FROM TS WHERE driver_id = ? AND vin = ? AND mark = ? AND model = ? AND made_date = ? AND color = ?", list_).fetchone()
    return ts is not None

def add_transport(list_):
    fio, vin, mark, model, date, color = list_
    fio = fio.split(" ")
    fio.append(" ")
    lastname, name, fathername = fio[:3]
    lastname, name, fathername = hash(lastname), hash(name), hash(fathername)
    dr_id = get_driver_id(lastname, name, fathername)
    
    if not dr_id:
        return True, "Водитель с такими данными не найден"
    
    transport = (
            dr_id, vin, mark, model, date, color,
        )
    if check_transport(transport):
        return True, f"Транспортное средство {mark} {model} {color} уже было зарегистрировано."

    cursor.execute(
        f"""INSERT INTO `TS` (driver_id, vin, mark, model, made_date, color) VALUES (?, ?, ?, ?, ?, ?)""", transport
    )
    connect.commit()
    return True, f"Транспортное средство {mark} {model} {color} было зарегистрировано."

def del_transport(list_):
    fio, vin, mark, model, date, color = list_
    fio = fio.split(" ")
    fio.append(" ")
    lastname, name, fathername = fio[:3]
    lastname, name, fathername = hash(lastname), hash(name), hash(fathername)
    dr_id = get_driver_id(lastname, name, fathername)

    transport = (
            dr_id, vin, mark, model, date, color,
        )
    if check_transport(transport):
        cursor.execute(
            "DELETE FROM TS WHERE driver_id = ? AND vin = ? AND mark = ? AND model = ? AND made_date = ? AND color = ?", transport
        )
        connect.commit()
        return True, f"Транспортное средство {mark} {model} {color} было удалено."
    return True, f"Транспортное средство {mark} {model} {color} не было найдено"