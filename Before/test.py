from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

imput_element = drive.get_element(By.CLASS_NAME, "")

time.sleep(10)

driver.quit()