import sqlite3
from functools import wraps
from sqlite3 import Error


def with_connection(dbfile="data.db"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            con = None  # برای تعریف شدن کانکت در محدوده بیرونی بلاک ترای
            try:
                con = sqlite3.connect(dbfile)
                cur = con.cursor()
                result = func(cur, *args, **kwargs)
                return result

            except Error as e:
                print(f"SQLite Error is : {e}")
            finally:
                if con:
                    con.close()

        return wrapper

    return decorator


@with_connection("data.db")
def make_dbfile(cur, table="analysis"):
    cur.execute(
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
make_dbfile()
