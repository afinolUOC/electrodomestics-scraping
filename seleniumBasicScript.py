import time
from selenium import webdriver
from selenium.webdriver.common.by import By


t = 2
driver = webdriver.Firefox()

driver.get("https://www.electrocosto.com/televisores/")
time.sleep(2*t)

refresh_box = driver.find_element(By.CLASS_NAME, 'w-100')

for i in range(3):
    driver.execute_script("arguments[0].scrollIntoView();", refresh_box)
    time.sleep(t)

time.sleep(t)
btn = refresh_box.find_element(By.CLASS_NAME, 'btn.btn-primary')
driver.execute_script("arguments[0].click();", btn)
time.sleep(t)
for i in range(7):
    driver.execute_script("arguments[0].scrollIntoView();", refresh_box)
    time.sleep(t)
#html = driver.page_source
#driver.find_elements(By.CLASS_NAME, 'recomender-block-item')