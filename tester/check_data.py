from decimal import Decimal

import jdatetime


def convert_jdate(date: str):
    """تبدیل فرمت به تاریخ شمسی برای بررسی دقیق تر"""
    year, month, day = map(int, date.strip().split("/"))
    jdate = jdatetime.date(year, month, day)
    return jdate


def checker(data, first_date):
    # اگر تاریخ ندادیم اولین روز رو قرار بده به عنوان معیار
    if first_date == "":
        first_date = convert_jdate(date=data[0][0])
    else:
        first_date = convert_jdate(date=first_date)

    for i, record in enumerate(data):
        # قسمت مربوط به تعیین صحت تاریخ
        excepted_date = first_date + jdatetime.timedelta(days=i)

        record_date = convert_jdate(date=f"{record[0].strip()}")

        if record_date != excepted_date:
            print(f"on day {i+1} date is not correct")

        # قسمت مربوط به تعیین مشمکلات دانه بندی
        if (record[2] + record[3] != record[1]) or (
            record[1] + record[4] + record[5] != Decimal("100.00")
        ):
            print(f"⚠️  Day {i+1}: Granulation calculation error")
            # قسمت مربوط به تعیین صحت دانه بندی زیر 10
            if record[2] + record[3] != record[1]:
                print(f"   Sum of 0-5 ({record[2]}) and 5-10 ({record[3]})")
                print(f"   does not equal below 10 ({record[1]})")
                print("   ─────────────────────────")
            if record[1] + record[4] + record[5] != Decimal("100.00"):
                print(f"   Below 10: {record[1]}")
                print(f"   10-60:    {record[4]}")
                print(f"   Above 60: {record[5]}")
                print(f"   does not equal 100%")
                print("   ─────────────────────────")
            if record[6] != 0 and record[7] != 0:
                avg_tonnage = record[6] / record[7]
                if avg_tonnage < Decimal("24.2") or avg_tonnage > Decimal("26.8"):
                    print(f"⚠️  Day {i+1}: Tonnage or number of truck is not correct!")
                    print("   ─────────────────────────")


checker(data=data, first_date="")
