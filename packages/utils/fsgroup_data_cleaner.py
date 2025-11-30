import re
from datetime import datetime, timedelta

import jdatetime
from fsgroup_regex import extract_kiln_data
from jalali_convertor import Jalali


def get_date():
    """get_date
    این تابع یا تاریخ شمسی را میگیرد یا به صورت پیش فرض امروز را مشخص میکند



    Returns:
        _type_: str
    """
    date_str = input("Enter the date (YYYY-MM-DD) or press Enter for today: ")
    if date_str.strip() == "":
        # تاریخ امروز میلادی
        today = datetime.today()

        # تاریخ روز گذشته میلادی
        yesterday = today - timedelta(days=1)

        # تبدیل به تاریخ شمسی
        jalali_date = jdatetime.date.fromgregorian(date=yesterday)

        # فرمت خروجی به شکل 1404/09/08
        date_str = jalali_date.strftime("%Y/%m/%d")

    else:
        date_str = date_str.strip()

    return date_str


def select_data(data, date):
    data_list = []

    # یه قسمت که از تاریخ شروع را از تایم استمپ ساعت 8 همون روز تا ساعت نه و نیم
    # روز بعدش به عنوان بازه مورد بررسی در نظر میگیرد.
    t = Jalali()
    min_time = t(date=date, time="08:00")
    max_time = min_time + 82800

    for item in data:
        send_time = item.get("time")
        if send_time == None:
            continue

        # Split safely
        send_time_str = str(send_time).split(",")
        if len(send_time_str) < 2:
            continue

        send_date = send_time_str[0]
        send_time_part = send_time_str[1][0:6]  # safer slice for HH:MM:SS
        send_timestamp = t(date=send_date, time=send_time_part)

        # Keep only items inside the desired range
        if not (min_time <= send_timestamp <= max_time):
            continue

        sender = str(item.get("sender", "")).strip()

        # Clean text properly
        text = str(item.get("text", "")).replace(r"\n", " ")
        extract_text = extract_kiln_data(text=text)

        # Skip if all values are empty/None
        if all(v in (None, []) for v in extract_text.values()):
            continue

        one_data = tuple([send_timestamp, sender, extract_text])
        data_list.append(one_data)

    return tuple(data_list)


def clean_name(name):
    """پاکسازی نام از اعداد و کاراکترهای خاص"""
    if not name:
        return name

    # حذف اعداد و کاراکترهای خاص (فقط حروف فارسی، انگلیسی و فاصله باقی بماند)
    cleaned = re.sub(r'[^a-zA-Z\u0600-\u06FF\s]', '', name)
    # حذف فاصله‌های اضافی
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def data_cleaner(data, date):
    dataset = [
        {
            "analyse_8": "",
            "send_time_8": "",
            "klin1_8": "",
            "klin2_8": "",
            "above40": "",
            "klin1_8_rep": "",
            "klin2_8_rep": "",
        },
        {
            "analyse_12": "",
            "send_time_12": "",
            "klin1_12": "",
            "klin2_12": "",
            "klin1_12_rep": "",
            "klin2_12_rep": "",
        },
        {
            "analyse_16": "",
            "send_time_16": "",
            "klin1_16": "",
            "klin2_16": "",
            "klin1_16_rep": "",
            "klin2_16_rep": "",
        },
        {
            "analyse_20": "",
            "send_time_20": "",
            "klin1_20": "",
            "klin2_20": "",
            "klin1_20_rep": "",
            "klin2_20_rep": "",
        },
        {
            "analyse_24": "",
            "send_time_24": "",
            "klin1_24": "",
            "klin2_24": "",
            "klin1_24_rep": "",
            "klin2_24_rep": "",
        },
        {
            "analyse_4": "",
            "send_time_4": "",
            "klin1_4": "",
            "klin2_4": "",
            "klin1_4_rep": "",
            "klin2_4_rep": "",
        },
    ]

    t = Jalali()
    timest = t(date=date, time="08:00")

    for msg_data in data:
        msg_timestamp = int(msg_data[0])
        msg_time = msg_data[2]['time'][0] if msg_data[2]['time'] else None
        cleaned_name = clean_name(msg_data[1])  # پاکسازی نام

        # شیفت 8:00 (7:30 تا 10:30)
        if (timest - 1800) <= msg_timestamp <= (timest + 9000):
            if msg_time == '08:00':
                dataset[0]["analyse_8"] = cleaned_name  # استفاده از نام پاکسازی شده
                dataset[0]["send_time_8"] = msg_timestamp
                if msg_data[2]['kiln1']:
                    dataset[0]["klin1_8"] = msg_data[2]['kiln1'][0]
                if msg_data[2]['kiln2']:
                    dataset[0]["klin2_8"] = msg_data[2]['kiln2'][0]
                if msg_data[2]['above40']:
                    dataset[0]["above40"] = msg_data[2]['above40'][0]
                if msg_data[2]['repeat_kiln1']:
                    dataset[0]["klin1_8_rep"] = msg_data[2]['repeat_kiln1'][0]
                if msg_data[2]['repeat_kiln2']:
                    dataset[0]["klin2_8_rep"] = msg_data[2]['repeat_kiln2'][0]

        # شیفت 12:00 (11:30 تا 14:30)
        elif (timest + 12600) <= msg_timestamp <= (timest + 23400):
            if msg_time == '12:00':
                dataset[1]["analyse_12"] = cleaned_name  # استفاده از نام پاکسازی شده
                dataset[1]["send_time_12"] = msg_timestamp
                if msg_data[2]['kiln1']:
                    dataset[1]["klin1_12"] = msg_data[2]['kiln1'][0]
                if msg_data[2]['kiln2']:
                    dataset[1]["klin2_12"] = msg_data[2]['kiln2'][0]
                if msg_data[2]['repeat_kiln1']:
                    dataset[1]["klin1_12_rep"] = msg_data[2]['repeat_kiln1'][0]
                if msg_data[2]['repeat_kiln2']:
                    dataset[1]["klin2_12_rep"] = msg_data[2]['repeat_kiln2'][0]

        # شیفت 16:00 (15:30 تا 18:30)
        elif (timest + 27000) <= msg_timestamp <= (timest + 37800):
            if msg_time == '16:00':
                dataset[2]["analyse_16"] = cleaned_name  # استفاده از نام پاکسازی شده
                dataset[2]["send_time_16"] = msg_timestamp
                if msg_data[2]['kiln1']:
                    dataset[2]["klin1_16"] = msg_data[2]['kiln1'][0]
                if msg_data[2]['kiln2']:
                    dataset[2]["klin2_16"] = msg_data[2]['kiln2'][0]
                if msg_data[2]['repeat_kiln1']:
                    dataset[2]["klin1_16_rep"] = msg_data[2]['repeat_kiln1'][0]
                if msg_data[2]['repeat_kiln2']:
                    dataset[2]["klin2_16_rep"] = msg_data[2]['repeat_kiln2'][0]

        # شیفت 20:00 (19:30 تا 22:30)
        elif (timest + 41400) <= msg_timestamp <= (timest + 52200):
            if msg_time == '20:00':
                dataset[3]["analyse_20"] = cleaned_name  # استفاده از نام پاکسازی شده
                dataset[3]["send_time_20"] = msg_timestamp
                if msg_data[2]['kiln1']:
                    dataset[3]["klin1_20"] = msg_data[2]['kiln1'][0]
                if msg_data[2]['kiln2']:
                    dataset[3]["klin2_20"] = msg_data[2]['kiln2'][0]
                if msg_data[2]['repeat_kiln1']:
                    dataset[3]["klin1_20_rep"] = msg_data[2]['repeat_kiln1'][0]
                if msg_data[2]['repeat_kiln2']:
                    dataset[3]["klin2_20_rep"] = msg_data[2]['repeat_kiln2'][0]

        # شیفت 24:00 (23:30 تا 02:30 روز بعد)
        elif (timest + 55800) <= msg_timestamp <= (timest + 66600):
            if msg_time == '24:00':
                dataset[4]["analyse_24"] = cleaned_name  # استفاده از نام پاکسازی شده
                dataset[4]["send_time_24"] = msg_timestamp
                if msg_data[2]['kiln1']:
                    dataset[4]["klin1_24"] = msg_data[2]['kiln1'][0]
                if msg_data[2]['kiln2']:
                    dataset[4]["klin2_24"] = msg_data[2]['kiln2'][0]
                if msg_data[2]['repeat_kiln1']:
                    dataset[4]["klin1_24_rep"] = msg_data[2]['repeat_kiln1'][0]
                if msg_data[2]['repeat_kiln2']:
                    dataset[4]["klin2_24_rep"] = msg_data[2]['repeat_kiln2'][0]

        # شیفت 4:00 (3:30 تا 6:30 روز بعد)
        elif (timest + 70200) <= msg_timestamp <= (timest + 81000):
            if msg_time == '04:00':
                dataset[5]["analyse_4"] = cleaned_name  # استفاده از نام پاکسازی شده
                dataset[5]["send_time_4"] = msg_timestamp
                if msg_data[2]['kiln1']:
                    dataset[5]["klin1_4"] = msg_data[2]['kiln1'][0]
                if msg_data[2]['kiln2']:
                    dataset[5]["klin2_4"] = msg_data[2]['kiln2'][0]
                if msg_data[2]['repeat_kiln1']:
                    dataset[5]["klin1_4_rep"] = msg_data[2]['repeat_kiln1'][0]
                if msg_data[2]['repeat_kiln2']:
                    dataset[5]["klin2_4_rep"] = msg_data[2]['repeat_kiln2'][0]

    return dataset


# how to use
# date = get_date()
# bad_data = select_data(data=??, date=date)
# clean_data = data_cleaner(data=bad_data, date=date)
