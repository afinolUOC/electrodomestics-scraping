import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def scroll_to(driver, scroll_element, t=1):
    # Scrolls the page until scrollElement is into view and waits t seconds
    driver.execute_script("arguments[0].scrollIntoView();", scroll_element)
    time.sleep(t)


def scroll_loop_to(driver, scroll_element, scroll_limit=3):
    # Don't stop scrolling util it get the same amount of items scroll_limit times in a row
    not_increase_count = 0
    n_items = len(driver.find_elements(By.CLASS_NAME, 'recomender-block-item'))

    # Start scrolling loop until limit was reach
    while not_increase_count < scroll_limit:
        scroll_to(driver, scroll_element)
        new_n_items = len(driver.find_elements(By.CLASS_NAME, 'recomender-block-item'))
        if n_items == new_n_items:
            not_increase_count += 1
        else:
            not_increase_count = 0
            n_items = new_n_items


def click_button(driver, btn_element, t=1):
    # Cliks the button btnElement and waits t seconds
    driver.execute_script("arguments[0].click();", btn_element)
    time.sleep(t)


def try_button(driver, element, class_name, button_limit=3, t=1):
    # Tries to get the button element and clicks it
    for index in range(button_limit):
        try:
            btn_primary_element = element.find_element(By.CLASS_NAME, class_name)
            click_button(driver, btn_primary_element)
            return
        except:
            time.sleep(t)

    print('Button not found')

def expand_section(section, firefox_path=r'C:\Program Files\Mozilla Firefox\firefox.exe', t=2):
    # Expands a section from: ("https://www.electrocosto.com/" + section) to show all products in this section
    url = "https://www.electrocosto.com/" + section
    print(f"Expanding {section} section")

    # Starting selenium webdriver
    options = Options()
    options.binary_location = firefox_path  # path for the executable for firefox in your PC
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(t)

    # Get class w-100, where the scroller observer is
    w_100_element = driver.find_element(By.CLASS_NAME, 'w-100')

    # Scroll until the observer gets into view this adds dynamically more items
    scroll_loop_to(driver, w_100_element)

    # Get and click the button 'Mostras más productos'
    try_button(driver, w_100_element, 'btn.btn-primary')
    time.sleep(t)

    # Scroll until the observer gets into view this adds dynamically more items
    scroll_loop_to(driver, w_100_element)

    # print and closes window
    n_items = len(driver.find_elements(By.CLASS_NAME, 'recomender-block-item'))
    print(f"Total items found: {n_items}")
    html = driver.page_source
    driver.close()

    return html
