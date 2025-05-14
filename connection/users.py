import hashlib
from config import connect, cursor

def hash(data):
    sha256_hash = hashlib.new('sha256')
    sha256_hash.update(data.encode())
    return sha256_hash.hexdigest()


driver = (
    hash("Иванов"), 
    hash("Иван"), 
    hash("Иванович"), 
    hash("+7 912 345 67 89"),
    "2007-01-20",
    "2020 808321",
    "г. Зима, ул. Кайская, д. 12",
    "г. Иркутск, ул. Лермонтова, д. 126",
    45,
)

vu = (
    1,
    "1234 567891",
    "2024-05-20",
    "2034-05-20",
    2,
)



def add_driver():
    cursor.execute(
        f"""INSERT INTO `DRIVERS` (lastname, name, fathername, phone, birth_date, passport, birth_place, place, region_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", driver
    )
    connect.commit()

def add_vu():
    cursor.execute(
        f"""INSERT INTO `VU` (driver_id, numer, start_date, end_date, dep_id) VALUES (?, ?, ?, ?, ?)""", vu
    )
    connect.commit()

add_driver()
add_vu()