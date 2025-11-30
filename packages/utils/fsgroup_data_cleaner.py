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


def clean_main(data):
    date = get_date()
    bad_data = select_data(data, date=date)
    clean_data = data_cleaner(data=bad_data, date=date)
    return clean_data


# how to use
# data = [
#     {'time': None, 'sender': None, 'text': None},
#     {
#         'time': '1404/9/7, 00:52:38',
#         'sender': 'عبدالله',
#         'text': 'سلام ساعت۲۴ \nکوره۱ =۰/۷۹\nکوره۲ =۰/۹۷',
#     },
#     {
#         'time': '1404/9/7, 00:53:50',
#         'sender': 'Mohammad Karimi',
#         'text': 'سلام به خاطرتعمیرات روی خط۰۹Bc2 لودینگ خالی بود',
#     },
#     {
#         'time': '1404/9/7, 05:32:02',
#         'sender': 'اسماعیل قوامی',
#         'text': 'سلام کوره 1 ساعت 4 بامداد 3.04 صدم شد...\nکوره 2 ساعت 4 بامداد 3.02 صدم شد....',
#     },
#     {
#         'time': '1404/9/7, 09:07:48',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'باسلام آنالیز ساعت ۸\nک یک ۴.۱۵\nک دو ۲.۹۶\nبالا چهل ۷.۱۴',
#     },
#     {
#         'time': '1404/9/7, 09:09:21',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'شارژ سنگ برای کوره از خط انجام می\u200cشود و محصول مطلوب میباشد \nمحصول در حال تولید خردایش یک و دو مطلوب و حدودا ۵ الی ۱۰ درصد قرمز دارد',
#     },
#     {
#         'time': '1404/9/7, 12:38:00',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'نضافت نیسان خارج از لیست نضافت، چون واقعا نمیشد داخلش بشینی از بس خاک گرفته بود',
#     },
#     {
#         'time': '1404/9/7, 12:45:24',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'سلام\nخداقوت جناب احمدپور\nممنون\n\nیه ماسک میزدی حداقل',
#     },
#     {'time': '1404/9/7, 12:50:05', 'sender': 'Mohammad Karimi', 'text': ''},
#     {
#         'time': '1404/9/7, 12:51:57',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'ما از بس دیگ تو اهکسازی تو اون چند سال ماسک نزدیم دماغمون آب بندی شده بدون ماسک اگ بزنم نمیتونم نفس بکشم',
#     },
#     {
#         'time': '1404/9/7, 12:52:33',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'آنالیز ساعت ۱۲\nک یک ۵.۰۱\nک دو ۲.۱۷',
#     },
#     {
#         'time': '1404/9/7, 12:53:48',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'نتیجه بازرسی خطوط تولید حدودا ۲۰ درصد بار قرمز در حال تولید میباشد',
#     },
#     {
#         'time': '1404/9/7, 12:55:29',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'دم رستوران ب هنرمند و جهانگیر گفتم بار قرمز در حال تولیده',
#     },
#     {
#         'time': '1404/9/7, 17:13:22',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'آنالیز ساعت ۱۶\nک یک ۴.۱۸\nک دو ۴.۴۲',
#     },
#     {
#         'time': '1404/9/7, 17:14:15',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'محصول سنگشکن یک در حال تولید قرمز',
#     },
#     {
#         'time': '1404/9/7, 17:16:01',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'بارگیری فولاد امروز متوقف بود کاملا و بارهایی ک تولید میشد قرمز بود و ب دپوها منتقل میشد',
#     },
#     {
#         'time': '1404/9/7, 20:46:06',
#         'sender': 'عبدالله',
#         'text': 'سلام ساعت۲۰ \nکوره۱ =۲/۱۵\nکوره۲ =۲/۶۵',
#     },
#     {
#         'time': '1404/9/7, 22:35:50',
#         'sender': 'عبدالله',
#         'text': 'باسلام خط خردایش درحال کار وبارتولیدی حدود ۲۰درصدقرمزی داشت.که به خط تولیداعلام شدجدابارتخلیه بشه',
#     },
#     {'time': '1404/9/7, 22:36:18', 'sender': 'عبدالله', 'text': 'خط تولید درحال کار'},
#     {
#         'time': '1404/9/7, 22:36:51',
#         'sender': 'عبدالله',
#         'text': 'شارج کوره مستقیم از خط ۰۵درحال انجام است',
#     },
#     {'time': None, 'sender': None, 'text': None},
#     {
#         'time': '1404/9/8, 00:02:29',
#         'sender': 'اسماعیل قوامی',
#         'text': 'سلام کوره 1 ساعت 24 4.07 صدم شد...\nکوره 2 ساعت 24 3.97 شد...',
#     },
#     {
#         'time': '1404/9/8, 06:26:13',
#         'sender': 'عبدالله',
#         'text': 'سلام ساعت۴ \nکوره۱ =۲/۴۷\nکوره۲ =۳/۱۴',
#     },
#     {
#         'time': '1404/9/8, 08:50:40',
#         'sender': 'اکبر  هدایت مقدم',
#         'text': 'سلام ساعت8\nک1------5/68\nک2-----3/43',
#     },
#     {
#         'time': '1404/9/8, 08:51:00',
#         'sender': 'اکبر  هدایت مقدم',
#         'text': 'بالای 40------9/11',
#     },
#     {
#         'time': '1404/9/8, 09:48:51',
#         'sender': 'اکبر  هدایت مقدم',
#         'text': 'خردایش 1محصول 06بارگیری وحمل به دپوپشت سنگ شکن ثانویه',
#     },
#     {
#         'time': '1404/9/8, 09:50:07',
#         'sender': 'اکبر  هدایت مقدم',
#         'text': 'صحبت شد محصول که مطلوب وخاک  کم دارد به دپو خردایش 2حمل شود',
#     },
#     {
#         'time': '1404/9/8, 09:51:19',
#         'sender': 'اکبر  هدایت مقدم',
#         'text': 'بارگیری بار فولاد کیفیت دانه بندی مطلوب رنگ درصد بسیار کمی قرمز است',
#     },
#     {
#         'time': '1404/9/8, 12:24:06',
#         'sender': 'Mohammad Karimi',
#         'text': 'درود خدمت همکاران گرامی\nکیفیت سنگ ورودی  از وضعیت مطلوبی برخوردار نیست',
#     },
#     {'time': '1404/9/8, 12:24:06', 'sender': 'Mohammad Karimi', 'text': ''},
#     {'time': '1404/9/8, 12:24:06', 'sender': 'Mohammad Karimi', 'text': ''},
#     {
#         'time': '1404/9/8, 12:24:36',
#         'sender': 'Mohammad Karimi',
#         'text': 'سلام\nاینها را فولاد فرستاده امروز\nبررسی کنید\nممنون',
#     },
#     {
#         'time': '1404/9/8, 16:39:00',
#         'sender': 'بهنام  ابولقاسمی آزمایشگاه',
#         'text': 'خط خردایش ۲در حال تولید است و محصول حدود 20 درصد قرمز است',
#     },
#     {
#         'time': '1404/9/8, 16:39:32',
#         'sender': 'بهنام  ابولقاسمی آزمایشگاه',
#         'text': 'محصول ارسالی از معدن حدود بیست درصد قرمز است',
#     },
#     {
#         'time': '1404/9/8, 16:39:52',
#         'sender': 'بهنام  ابولقاسمی آزمایشگاه',
#         'text': 'ارتفاع دپو 06 کم است',
#     },
#     {
#         'time': '1404/9/8, 16:47:46',
#         'sender': 'اکبر  هدایت مقدم',
#         'text': 'ساعت16\nک1------2/95\nک2-------1/61',
#     },
#     {
#         'time': '1404/9/8, 21:31:03',
#         'sender': '98229 Morteza_Ahmadpor',
#         'text': 'باسلام آنالیز ساعت ۲۰\nک یک ۴.۰۵\nک دو ۸.۲۲\nتکرار ک دو ۴.۱۰',
#     },
# ]
# date = get_date()
# bad_data = select_data(data=data, date=date)
# clean_data = data_cleaner(data=bad_data, date=date)
# print(clean_data)
