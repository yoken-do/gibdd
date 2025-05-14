import sqlite3

connect = sqlite3.connect("./database.db")
cursor = connect.cursor()

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS `DRIVERS`
(
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    lastname TEXT NOT NULL,
    name TEXT NOT NULL,
    fathername TEXT,
    phone TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    birth_place TEXT NOT NULL,
    passport TEXT NOT NULL,
    place TEXT NOT NULL,
    region_id INTEGER NOT NULL,
    FOREIGN KEY ('region_id') REFERENCES `REGIONS`(`id`)
)
"""
)

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS `VU`
(
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    driver_id INTEGER NOT NULL UNIQUE,
    numer TEXT NOT NULL UNIQUE,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    dep_id INTEGER NOT NULL,
    FOREIGN KEY ('driver_id') REFERENCES `DRIVERS`(`id`),
    FOREIGN KEY ('dep_id') REFERENCES `DEPARTMENTS`(`id`)
)   
"""
)

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS `FINES`
(
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    driver_id INTEGER NOT NULL,
    uid INTEGER NOT NULL UNIQUE,
    reason TEXT NOT NULL,
    summa INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY ('driver_id') REFERENCES `DRIVERS`(`id`)
)   
"""
)

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS `TS`
(
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    driver_id INTEGER NOT NULL,
    vin TEXT NOT NULL,
    mark TEXT NOT NULL,
    model TEXT NOT NULL,
    made_date TEXT NOT NULL,
    color TEXT NOT NULL,
    FOREIGN KEY ('driver_id') REFERENCES `DRIVERS`(`id`)
)   
"""
)

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS `DEPARTMENTS`
(
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    title TEXT NOT NULL,
    address TEXT NOT NULL,
    region_id INTEGER NOT NULL,
    FOREIGN KEY ('region_id') REFERENCES `REGIONS`(`id`)
)   
"""
)

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS `SERVICES`
(
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    title TEXT NOT NULL
)
"""
)

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS `BRANCHES_DEPARTMENT`
(
    id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    dep_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    FOREIGN KEY ('service_id') REFERENCES `SERVICE`(`id`),
    FOREIGN KEY ('dep_id') REFERENCES `DEPARTMENTS`(`id`)
)
"""
)

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS `REGIONS`
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE
)
"""
)

