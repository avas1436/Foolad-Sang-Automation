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
                con.commit()
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
                id INTEGER UNIQUE,
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
                upper60 REAL)
            """
    )


@with_connection("day_avg.db")
def make_dbfile_avg(cur, table="analysis"):
    cur.execute(
        f"""
                CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER UNIQUE,
                date TEXT,
                weather TEXT,
                tonnage REAL,
                truck REAL,
                CO2 REAL,
                COupper40 REAL,
                lower10 REAL,
                par0 REAL,
                par5 REAL,
                par60 REAL,
                upper60 REAL)
            """
    )


@with_connection("day_avg.db")
def export_data_avg(cur, data: list, table="analysis"):
    cur.execute(
        f"""
    INSERT OR IGNORE INTO {table} (id,
                        date,
                        weather,
                        tonnage,
                        truck,
                        CO2,
                        COupper40,
                        lower10,
                        par0,
                        par5,
                        par60,
                        upper60)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        data,
    )


## how to make db file
# make_dbfile("day_avg.db")


## how to insert data in daily average
# make_dbfile_avg()
# ls = [
#     1755491400,
#     '1404/05/27',
#     'Sunny',
#     316.4,
#     12,
#     3.82,
#     7.1,
#     10.13,
#     5.2,
#     4.93,
#     89.87,
#     0,
# ]
# export_data_avg(data=ls)
