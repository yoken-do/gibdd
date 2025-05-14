from config import database_path

from config import cursor, connect
from collections import defaultdict
import hashlib
from datetime import datetime

def hash(data):
    sha256_hash = hashlib.new('sha256')
    sha256_hash.update(data.encode())
    return sha256_hash.hexdigest()



def department_list():
    departments = cursor.execute("SELECT title, address FROM DEPARTMENTS").fetchall()
    services = cursor.execute("""
        SELECT d.title, s.title 
        FROM BRANCHES_DEPARTMENT b
        JOIN DEPARTMENTS d ON b.dep_id = d.id
        JOIN SERVICES s ON b.service_id = s.id
    """).fetchall()
    dep_list = defaultdict(list)

    for dep, address in departments:
        dep_list[dep] = {
            "address": address,
            "services": []
        }

    for dep, service in services:
        if service not in dep_list[dep]["services"]:
            dep_list[dep]["services"].append(service)

    return dep_list

def get_driver_id(list_):
    fio, numer, birthdate, phone = list_
    fio = fio.split(" ")
    fio.append('')
    lastname, name, fathername = fio[:3]

    hash_lastname, hash_name, hash_fathername = hash(lastname), hash(name), hash(fathername)

    driver_id = cursor.execute("SELECT id FROM DRIVERS WHERE lastname = ? AND name = ? AND fathername = ? AND phone = ? AND birth_date = ?", (hash_lastname, hash_name, hash_fathername, hash(phone), birthdate, )).fetchone()
    return driver_id[0] if driver_id else None

def sign(fio: str, vu: int, birthdate: str, phone: str):
    
    fio = fio.split(" ")
    fio.append('')
    lastname, name, fathername = fio[:3]
    lastname, name, fathername = hash(lastname), hash(name), hash(fathername)
    phone = hash(phone)
    driver_id = cursor.execute("SELECT id FROM DRIVERS WHERE lastname = ? AND name = ? AND fathername = ? AND phone = ? AND birth_date = ?", (lastname, name, fathername, phone, birthdate, )).fetchone()
    
    if not driver_id:
        return False
    vu = cursor.execute("SELECT numer FROM `VU` WHERE driver_id = ?", (driver_id[0], )).fetchone()
    return vu is not None

def passport(list_: list) -> dict:
    try:
        fio, numer, birthdate, phone = list_
        fio = fio.split(" ")
        fio.append('')
        lastname, name, fathername = fio[:3]

        hash_lastname, hash_name, hash_fathername = hash(lastname), hash(name), hash(fathername)

        pasport, birth_place, place, region, start_date, end_date, dep = cursor.execute(
            """
            SELECT d.passport, d.birth_place, d.place, r.title, vu.start_date, vu.end_date, dep.title
            FROM DRIVERS d
            JOIN REGIONS r ON d.region_id = r.id
            JOIN VU vu ON vu.driver_id = d.id
            JOIN DEPARTMENTS dep ON vu.dep_id = dep.id
            WHERE d.lastname = ? AND d.name = ?
                 AND d.fathername = ? AND d.phone = ?
                 AND d.birth_date = ?
                 AND vu.numer = ?
            """,
            (hash_lastname, hash_name, hash_fathername, hash(phone), birthdate, numer, )
        ).fetchone()

        status = datetime.now().date() < datetime.strptime(end_date, "%Y-%m-%d").date()
        status_text = ''
        if status:
            status_text = f'Права действительны до {end_date}'
        else:
            status_text = "Права больше не действительны"

        return {
            'lastname': lastname,
            'name': name,
            'fathername': fathername,
            'phone': phone,
            'birth_date': birthdate,
            'birth_place': birth_place,
            'place': place,
            'region': region,
            'numer': numer,
            'vu_start_date': start_date,
            'vu_end_date': end_date,
            'department': dep,
            'status': status_text,
            'passport': pasport
        }

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None


def fines(list_: list):
    try:
        fio, numer, birthdate, phone = list_
        fio = fio.split(" ")
        fio.append('')
        lastname, name, fathername = fio[:3]

        hash_lastname, hash_name, hash_fathername = hash(lastname), hash(name), hash(fathername)

        driver_id = get_driver_id(list_)
        
        fines = cursor.execute("SELECT uid, reason, summa, date, status FROM FINES WHERE driver_id = ?", (driver_id, )).fetchall()
        fines_list = []
        for fine in fines:
            fines_list.append(
                {
                    "numer": fine[0],
                    "reason": fine[1],
                    "sum": fine[2],
                    "date": fine[3],
                    "status": fine[4]
                }
            )
        return fines_list[::-1]

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None
    
def ts(list_: list):
    try:
        fio, numer, birthdate, phone = list_
        fio = fio.split(" ")
        fio.append('')
        lastname, name, fathername = fio[:3]

        hash_lastname, hash_name, hash_fathername = hash(lastname), hash(name), hash(fathername)

        driver_id = get_driver_id(list_)
        
        items = cursor.execute("SELECT vin, mark, model, made_date, color FROM TS WHERE driver_id = ?", (driver_id, )).fetchall()
        ts_list = []
        for item in items:
            ts_list.append(
                {
                    "vin": item[0],
                    "mark": item[1],
                    "model": item[2],
                    "date": item[3],
                    "color": item[4]
                }
            )
        return ts_list if ts_list else None

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None


def get_fines_sum(list_):
    driver_id = get_driver_id(list_)
    fine_sum = cursor.execute("SELECT sum(summa) FROM FINES WHERE driver_id = ? AND status = ?", (driver_id, "Не оплачен",)).fetchone()
    return fine_sum[0] if fine_sum else None