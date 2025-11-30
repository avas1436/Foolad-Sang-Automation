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


def scroling_chat(driver):
    try:
        scrollable_div = driver.find_element(
            By.CSS_SELECTOR, "div.bubbles.scrolled-down div.scrollable.scrollable-y"
        )

        # Scroll to top
        driver.execute_script("arguments[0].scrollTop = 0", scrollable_div)
        time.sleep(2)

        # Get initial metrics
        last_height = driver.execute_script(
            "return arguments[0].scrollHeight", scrollable_div
        )
        current_position = 0
        consecutive_no_change = 0

        while consecutive_no_change < 3:  # Stop after 3 attempts with no change
            # Scroll down
            current_position += 800
            driver.execute_script(
                f"arguments[0].scrollTop = {current_position}", scrollable_div
            )

            # Wait for potential content load
            WebDriverWait(driver, 3).until(
                lambda d: driver.execute_script(
                    "return arguments[0].scrollHeight", scrollable_div
                )
                > last_height
            )

            # Get new height
            new_height = driver.execute_script(
                "return arguments[0].scrollHeight", scrollable_div
            )
            current_position = driver.execute_script(
                "return arguments[0].scrollTop", scrollable_div
            )

            print(f"📊 Scroll: Position {current_position}, Height {new_height}")

            # Check if content changed
            if new_height == last_height:
                consecutive_no_change += 1
            else:
                consecutive_no_change = 0
                last_height = new_height

            # Check if we're at the bottom
            if current_position + 1000 >= new_height:
                print("🎯 Reached apparent bottom")
                break

        return True

    except Exception as e:
        print(f"🚫 Scroll error: {str(e)}")
        return False
