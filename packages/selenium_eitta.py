import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# پیدا کردن مسیر برنامه یعنی همان جایی که برنامه ایجاد می شود.
base_dir = os.path.dirname(os.path.abspath(__file__))

# فولدر پروفایل جدید داخل همان فولدر برنامه
profile_path = os.path.join(base_dir, "chrome_profile")

# اگر فولدر وجود ندارد، بساز
if not os.path.exists(profile_path):
    os.makedirs(profile_path)


# کار این قسمت ذخیره اطلاعات ورود است
options = webdriver.ChromeOptions()

# تمامی اطلاعات وارد شده در برنامه در اینجا ذخیره خواهد شد.
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument("--profile-directory=Default")  # مشخص کردن پروفایل
options.add_argument("--no-first-run")  # جلوگیری از اجرای اولیه
options.add_argument("--no-default-browser-check")  # جلوگیری از چک مرورگر پیشفرض
options.add_argument("--disable-extensions")  # غیرفعال کردن اکستنشن‌ها
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


# آپشن های اضافه برای اطمینان بیشتر
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


# ایجاد درایور با آپشن‌ها
driver = webdriver.Chrome(options=options)


driver.get("https://web.eitaa.com/")


login_attempts = 0
max_attempts = 60  # Maximum 5 minutes wait

while login_attempts < max_attempts:
    login_attempts += 1

    try:
        # صفحه ورود اولیه
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h4.text-center.i18n"))
        )
        if "ورود به ایتا" in element.text:
            print("📱 On phone number entry page")
            input("Please enter your phone number and press enter: ")
            continue
    except:
        pass

    try:
        # صفحه کد تأیید
        auth_page = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".page-authCode.active"))
        )

        # بررسی وضعیت فیلد کد
        code_input = driver.find_element(
            By.CSS_SELECTOR, "input.input-field-input[type='tel']"
        )
        if code_input.is_enabled():
            print("🔐 On verification code page")
            input("Please enter verification code and press enter: ")
            continue
    except:
        pass

    try:
        # بررسی ورود موفق
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".page-chats"))
        )

        chat_items = driver.find_elements(By.CSS_SELECTOR, ".chatlist-chat")
        if len(chat_items) > 0:
            print(f"✅ Login successful! Found {len(chat_items)} chats.")
            break
        else:
            print("⏳ Waiting for chats to load...")
            time.sleep(1)
            continue

    except:
        # print(f"Attempt {login_attempts}/{max_attempts}...")  # For debugging
        time.sleep(1)
        continue

if login_attempts >= max_attempts:
    print("❌ Timeout exceeded. Please check the status.")
else:
    print("🎉 Ready to use Eitaa!")


# پیدا کردن چت مورد نظر با شناسه -51577627
# این چت همان گروه کنترل کیفی و آزمایشگاه است

chat_id = 34936560  # ثابتین
# caht_id = -51577627 # گروه کنترل کیفیت و آزمایشگاه


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


# استفاده از تابع
find_and_select_chat(driver, chat_id)

input("press inter")
