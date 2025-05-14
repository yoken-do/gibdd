from config import connect, cursor

fine = (
    1,
    198177,
    "Парковка в неположенном месте",
    1200,
    "2010-10-15",
    "Не оплачен"
)


cursor.execute(
    f"""INSERT INTO `FINES` (driver_id, uid, reason, summa, date, status) VALUES (?, ?, ?, ?, ?, ?)""", fine
)
connect.commit()