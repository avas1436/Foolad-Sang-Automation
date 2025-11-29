import time

import lxml
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def extract_text_messages_until_timestamp(driver):

    # کد استخراج دیتا از گروه فولاد سنگ
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    # کانتینر اصلی
    container = soup.find("div", class_="bubbles-inner has-rights is-chat is-channel")
    # همه‌ی پیام‌ها داخل کانتینر
    messages = container.find_all("div", class_="bubble")  # یا کلاس واقعی پیام‌ها

    # لیست خالی برای درج اطلاعات
    chat_data = []

    # حلقه استخراج اطلاعات
    for msg in messages:
        # متن پیام
        message_tag = msg.find("div", class_="message")
        text = (
            "".join([c for c in message_tag.contents if isinstance(c, str)]).strip()
            if message_tag
            else None
        )

        # زمان پیام
        time_tag = msg.find("span", class_="time tgico")
        time = time_tag.get("title") if time_tag else None

        # فرستنده
        sender_tag = msg.find("span", class_="peer-title")
        sender = sender_tag.get_text(strip=True) if sender_tag else None

        chat_data.append({"time": time, "sender": sender, "text": text})

    return chat_data
