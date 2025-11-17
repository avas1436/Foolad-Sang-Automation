import re


def extract_kiln_data(text):
    """
    استخراج داده‌های کوره‌ها از متن‌های مختلف با پشتیبانی از فرمت‌های مختلف اعداد اعشاری
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

    # الگوی اصلی برای استخراج داده‌ها
    patterns = {
        "time": r"ساعت\s*([۰-۹0-9:]+)",
        "kiln1": [
            # الگوهای مختلف برای کوره 1
            r"ک\s*(?:وره)?\s*1\s*[=:\-–—]+\s*([۰-۹0-9.]+)",  # کوره1 = 3.55
            r"ک\s*یک\s*([۰-۹0-9.]+)",  # ک یک ۴.۲۸
            r"کوره\s*1\s*ساعت\s*[۰-۹0-9]+\s*([۰-۹0-9.]+)",
            r"ک\s*(?:وره)?\s*1\s*[=:\-–—]+\s*([۰-۹0-9]+[./][۰-۹0-9]+)",  # کوره1 = 3.55 یا 3/55
            r"ک\s*(?:وره)?\s*1\s*[=:\-–—]+\s*([۰-۹0-9]+\s*[./]\s*[۰-۹0-9]+)",  # فاصله احتمالی around separator
            r"ک\s*یک\s*([۰-۹0-9]+[./][۰-۹0-9]+)",  # ک یک ۴.۲۸
            r"ک\s*یک\s*([۰-۹0-9]+\s*[./]\s*[۰-۹0-9]+)",  # ک یک ۴ . ۲۸
            r"کوره\s*1\s*ساعت\s*[۰-۹0-9]+\s*([۰-۹0-9]+[./][۰-۹0-9]+)",  # کوره 1 ساعت 16 6.46
            r"کوره\s*1\s*ساعت\s*[۰-۹0-9]+\s*([۰-۹0-9]+\s*[./]\s*[۰-۹0-9]+)",  # کوره 1 ساعت 16 6 . 46
        ],
        "kiln2": [
            # الگوهای مختلف برای کوره 2
            r"ک\s*(?:وره)?\s*2\s*[=:\-–—]+\s*([۰-۹0-9.]+)",  # کوره2 = 2.79
            r"ک\s*دو\s*([۰-۹0-9.]+)",  # ک دو ۳.۰۳
            r"کوره\s*2\s*ساعت\s*[۰-۹0-9]+\s*([۰-۹0-9.]+)",  # کوره 2 ساعت 16 4.91
            r"ک\s*(?:وره)?\s*2\s*[=:\-–—]+\s*([۰-۹0-9]+[./][۰-۹0-9]+)",  # کوره2 = 2.79
            r"ک\s*(?:وره)?\s*2\s*[=:\-–—]+\s*([۰-۹0-9]+\s*[./]\s*[۰-۹0-9]+)",  # با فاصله
            r"ک\s*دو\s*([۰-۹0-9]+[./][۰-۹0-9]+)",  # ک دو ۳.۰۳
            r"ک\s*دو\s*([۰-۹0-9]+\s*[./]\s*[۰-۹0-9]+)",  # ک دو ۳ . ۰۳
            r"کوره\s*2\s*ساعت\s*[۰-۹0-9]+\s*([۰-۹0-9]+[./][۰-۹0-9]+)",  # کوره 2 ساعت 16 4.91
            r"کوره\s*2\s*ساعت\s*[۰-۹0-9]+\s*([۰-۹0-9]+\s*[./]\s*[۰-۹0-9]+)",  # با فاصله
        ],
        "above40": [
            r"بالای\s*40\s*[=:\-–—]+\s*([۰-۹0-9.]+)"  # بالای 40-------2/88
            r"بالای\s*40\s*[=:\-–—]+\s*([۰-۹0-9]+[./][۰-۹0-9]+)",  # بالای 40-------2/88
            r"بالای\s*40\s*[=:\-–—]+\s*([۰-۹0-9]+\s*[./]\s*[۰-۹0-9]+)",  # با فاصله
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
            # نرمال‌سازی جداکننده اعشار
            value = match.group(1).replace(" ", "").replace("/", ".")
            result["kiln1"] = value
            break

    # استخراج کوره 2
    for pattern in patterns["kiln2"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).replace(" ", "").replace("/", ".")
            result["kiln2"] = value
            break

    # استخراج بالای 40
    for pattern in patterns["above40"]:
        above40_match = re.search(pattern, text, re.IGNORECASE)
        if above40_match:
            value = above40_match.group(1).replace(" ", "").replace("/", ".")
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
