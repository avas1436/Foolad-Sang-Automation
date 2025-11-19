import sqlite3
from sqlite3 import Error


def make_dbfile(name="data.db", table="analysis"):
    try:
        con = sqlite3.connect(name)
        con.execute(
            f"""
                    CREATE TABLE IF NOT EXISTS {table} (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    time TEXT,
                    weather TEXT,
                    klin1 REAL,
                    klin2 REAL,
                    upper40 REAL,
                    lower10 REAL,
                    par5 REAL,
                    par0 REAL,
                    par60 REAL,
                    par70 REAL)
                """
        )

    except Error as e:
        print(f"SQLite Error is : {e}")
    finally:
        if con:
            con.close()


def export_data(data: list, dbfile: str):
    try:
        con = sqlite3.connect(r"data.db")
        cur = con.cursor()
        cur.execute()

    except Error as e:
        print(f"SQLite Error is : {e}")
    finally:
        if con:
            con.close()


## how to use
# make_dbfile()
