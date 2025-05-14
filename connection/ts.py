from config import connect, cursor


ts1 = (1, "WVWZZZ1KZ8W123456", "Volkswagen", "Tiguan", "2020-11-20", "серебристый", )
ts2 = (1, "JM1GW2324H0123456", "Honda", "CBR600RR", "2019-07-30", "чёрный", )
ts3 = (1, "5YJSA1E21HF123789", "Tesla", "Model 3", "2023-02-10", "красный", )

cursor.executemany(
    f"""INSERT INTO `TS` (driver_id, vin, mark, model, made_date, color) VALUES (?, ?, ?, ?, ?, ?)""", [ts1, ts2, ts3]
)
connect.commit()