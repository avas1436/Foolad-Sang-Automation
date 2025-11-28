import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def find_and_select_chat(driver, chat_id, max_scrolls=40):
    """
    تابع یکپارچه برای پیدا کردن و انتخاب چت
    Integrated function to find and select chat
    """

    # مرحله ۱: جستجوی مستقیم
    try:
        print("🔍 Searching directly...")
        chat_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-peer-id="{chat_id}"]'))
        )
        chat_element.click()
        print("✅ Success - Direct selection")
        time.sleep(3)
        return True
    except:
        print("❌ Direct search failed, starting scroll...")

    # مرحله ۲: اسکرول هوشمند
    try:
        scrollable = driver.find_element(
            By.CSS_SELECTOR, '.scrollable.scrollable-y.tabs-tab.chatlist-parts.active'
        )

        for scroll_count in range(1, max_scrolls + 1):
            print(f"🔄 Scroll {scroll_count}/{max_scrolls}")

            # اسکرول
            driver.execute_script("arguments[0].scrollTop += 1000;", scrollable)
            time.sleep(2)

            # بررسی وجود چت
            try:
                chat_element = driver.find_element(
                    By.CSS_SELECTOR, f'[data-peer-id="{chat_id}"]'
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", chat_element
                )
                time.sleep(1)
                chat_element.click()
                print(f"✅ Success - Found after {scroll_count} scrolls")
                return True
            except:
                continue

    except Exception as e:
        print(f"🚫 Scroll error: {e}")

    # مرحله ۳: روش جایگزین
    print("🔄 Trying alternative method...")
    for i in range(15):
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(1.5)

        try:
            driver.find_element(By.CSS_SELECTOR, f'[data-peer-id="{chat_id}"]').click()
            print("✅ Success - Alternative method")
            return True
        except:
            continue

    print("💥 All methods failed")
    return False
