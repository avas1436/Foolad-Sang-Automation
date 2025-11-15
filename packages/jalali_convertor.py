from datetime import timestamp

import jdatetime


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

        return int(gregorian_dt.timestamp())

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
# m = cur.fetchall()
# for date, time in m:
#     t = Jalali()
#     print(t.converter(date, time))
