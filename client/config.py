from pathlib import Path
import sqlite3

database_path = Path(__file__).parent.parent / "connection" / 'database.db'
connect = sqlite3.connect(database_path, check_same_thread=False)
cursor = connect.cursor()