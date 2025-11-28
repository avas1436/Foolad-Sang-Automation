import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()

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
