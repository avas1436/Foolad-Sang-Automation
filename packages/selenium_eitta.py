from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()

driver.get("https://web.eitaa.com/")


element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.CSS_SELECTOR,
            "html > body > div:first-of-type > div > div:nth-of-type(2) > div:first-of-type > div > h4",
        )
    )
)

if element:
    while True:
        input("Please login to your account and tap enter")
        if element:
            continue
        else:
            break
