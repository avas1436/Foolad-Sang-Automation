import re


def extract_kiln_data(text):
    """
    استخراج داده‌های کوره‌ها از متن‌های مختلف با پشتیبانی از اعداد اعشاری و صحیح
    """
    # نرمال‌سازی متن - تبدیل اعداد فارسی به انگلیسی
    text = (
        text.replace("۰", "0")
        .replace("۱", "1")
        .replace("۲", "2")
        .replace("۳", "3")
        .replace("۴", "4")
        .replace("۵", "5")
        .replace("۶", "6")
        .replace("۷", "7")
        .replace("۸", "8")
        .replace("۹", "9")
        .replace("٠", "0")
        .replace("١", "1")
        .replace("٢", "2")
        .replace("٣", "3")
        .replace("٤", "4")
        .replace("٥", "5")
        .replace("٦", "6")
        .replace("٧", "7")
        .replace("٨", "8")
        .replace("٩", "9")
    )

    def normalize_number(num_str):
        """نرمال‌سازی عدد و تشخیص نوع آن (اعشاری یا صحیح)"""
        if not num_str:
            return None

        # حذف فاصله‌ها و تبدیل جداکننده‌ها
        num_str = num_str.replace(" ", "").replace("/", ".")

        # بررسی اینکه آیا عدد اعشاری است یا صحیح
        if "." in num_str:
            # عدد اعشاری
            try:
                return float(num_str)
            except ValueError:
                return num_str
        else:
            # عدد صحیح
            try:
                return int(num_str)
            except ValueError:
                return num_str

    # الگوی اصلی برای استخراج داده‌ها - پشتیبانی از اعداد صحیح و اعشاری
    patterns = {
        "time": r"ساعت\s*([۰-۹0-9:]+)",
        "kiln1": [
            # الگوهای مختلف برای کوره 1 - پشتیبانی از اعداد صحیح و اعشاری
            r"ک\s*(?:وره)?\s*1\s*[=:\-–—]+\s*([۰-۹0-9]+(?:\s*[./]\s*[۰-۹0-9]+)?)",  # کوره1 = 3.55 یا 3/55 یا 4
            r"ک\s*یک\s*([۰-۹0-9]+(?:\s*[./]\s*[۰-۹0-9]+)?)",  # ک یک ۴.۲۸ یا ۵
            r"کوره\s*1\s*ساعت\s*[۰-۹0-9]+\s*([۰-۹0-9]+(?:\s*[./]\s*[۰-۹0-9]+)?)",  # کوره 1 ساعت 16 6.46 یا 7
            r"ک\s*1\s*[=:\-–—]+\s*([۰-۹0-9]+(?:\s*[./]\s*[۰-۹0-9]+)?)",  # ک1-------3/55 یا 4
        ],
        "kiln2": [
            # الگوهای مختلف برای کوره 2 - پشتیبانی از اعداد صحیح و اعشاری
            r"ک\s*(?:وره)?\s*2\s*[=:\-–—]+\s*([۰-۹0-9]+(?:\s*[./]\s*[۰-۹0-9]+)?)",  # کوره2 = 2.79 یا 3
            r"ک\s*دو\s*([۰-۹0-9]+(?:\s*[./]\s*[۰-۹0-9]+)?)",  # ک دو ۳.۰۳ یا ۴
            r"کوره\s*2\s*ساعت\s*[۰-۹0-9]+\s*([۰-۹0-9]+(?:\s*[./]\s*[۰-۹0-9]+)?)",  # کوره 2 ساعت 16 4.91 یا 5
            r"ک\s*2\s*[=:\-–—]+\s*([۰-۹0-9]+(?:\s*[./]\s*[۰-۹0-9]+)?)",  # ک2-------3/04 یا 4
        ],
        "above40": [
            r"بالای\s*40\s*[=:\-–—]+\s*([۰-۹0-9]+(?:\s*[./]\s*[۰-۹0-9]+)?)",  # بالای 40-------2/88 یا 3
        ],
    }

    result = {}

    # استخراج زمان
    time_match = re.search(patterns["time"], text, re.IGNORECASE)
    if time_match:
        result["time"] = time_match.group(1).strip()

    # استخراج کوره 1
    for pattern in patterns["kiln1"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = normalize_number(match.group(1))
            if value is not None:
                result["kiln1"] = value
                break

    # استخراج کوره 2
    for pattern in patterns["kiln2"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = normalize_number(match.group(1))
            if value is not None:
                result["kiln2"] = value
                break

    # استخراج بالای 40
    for pattern in patterns["above40"]:
        above40_match = re.search(pattern, text, re.IGNORECASE)
        if above40_match:
            value = normalize_number(above40_match.group(1))
            if value is not None:
                result["above40"] = value
                break

    return result


# تست با یک متن پیچیده
text_moghadam = """
سلام ساعت8
ک1-------3/55
ک2-------3/04
بالای 40-------2/88
"""
text_taheri = """
سلام ساعت۴
کوره۱ =۳/۳۵
کوره۲ =۲/۷۹
"""

text_esmaeel = """
سلام کوره 1 ساعت 16 6.46 شد...
کوره 2 ساعت 16 4.91 شد...
"""

text_morteza = """
آنالیز ساعت ۱۲
ک یک ۴
ک دو ۳.۰۳
"""

# تست الگو با متن‌های نمونه
texts = [text_moghadam, text_taheri, text_esmaeel, text_morteza]

for i, text in enumerate(texts, 1):
    print(f"متن {i}:")
    data = extract_kiln_data(text)
    print(data)
    print("-" * 30)
