import json
from config import connect, cursor


def get_dep_id(title):
    return cursor.execute("SELECT id FROM `DEPARTMENTS` WHERE title = ?", (title, )).fetchone()[0]

def get_service_id(title):
    return cursor.execute("SELECT id FROM `SERVICES` WHERE title = ?", (title, )).fetchone()[0]


def regions():
    with open('../data/regions.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    cursor.executemany(
        f"""INSERT INTO `REGIONS` (title) VALUES (?)""", [(item, ) for item in data]
    )
    connect.commit()

def branches():
    with open('../data/branches.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    cursor.executemany(
        f"""INSERT INTO `BRANCHES_DEPARTMENT` (dep_id, service_id, address) VALUES (?, ?, ?)""", [(get_dep_id(item[0]),get_service_id(item[1]), item[2],  ) for item in data]
    )
    connect.commit()

def service():
    with open('../data/service.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    cursor.executemany(
        f"""INSERT INTO `SERVICES` (title) VALUES (?)""", [(item, ) for item in data]
    )
    connect.commit()

def department():
    with open('../data/department.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    cursor.executemany(
        f"""INSERT INTO `DEPARTMENTS` (title, address, region_id) VALUES (?, ?, ?)""", [(item[0], item[1], 45, ) for item in data]
    )
    connect.commit()

regions()
service()
department()
branches()
