import datetime
import logging

import jdatetime

logging.basicConfig(
    level=logging.DEBUG,
    filename="datetime.log",
    filemode="w",
    format="%(name)s-%(levelname)s-%(funcName)s:%(lineno)d-%(message)s",
)


class Jalali:
    def __call__(self, date: str, time: str) -> int:
        return self.converter(date, time)

    def __str__(self) -> str:
        return "input date in '1404/08/12' format and time in '08:00' format"

    def converter(self, date: str, time: str) -> int:
        year, month, day = map(int, date.split("/"))
        hour, minute = map(int, time.split(":"))

        persian_dt = jdatetime.datetime(
            year=year, month=month, day=day, hour=hour, minute=minute
        )
        gregorian_dt = persian_dt.togregorian()
        time_stamp = int(gregorian_dt.timestamp())
        logging.debug(f"for datetime {str(persian_dt)} timestamp is {time_stamp}")
        return time_stamp

    def edith_time(self, hour: int) -> str:
        if 0 <= hour <= 9:
            time = f"0{hour}:00"
        else:
            time = f"{hour}:00"
        return time


# how to use

# import sqlite3

# con = sqlite3.connect(
#     r"F:\اتوماتیک ساز\3. data extract\استخراج دیتا گزارش روزانه\7\7. mehr\data.db"
# )
# cur = con.cursor()
# cur.execute("SELECT date, hour FROM data LIMIT 5")
# date_list = [
#     ("1404/06/01", "08:00"),
#     ("1404/06/01", "10:00"),
#     ("1404/06/01", "12:00"),
#     ("1404/06/01", "14:00"),
#     ("1404/06/01", "16:00"),
#     ("1404/06/01", "20:00"),
# ]

# m = cur.fetchall()
# for date, time in date_list:
#     t = Jalali()
#     print(t.converter(date, time))
