import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def scroll_to(driver, scroll_element, t=2):
    # Scrolls the page until scrollElement is into view and waits t seconds
    driver.execute_script("arguments[0].scrollIntoView();", scroll_element)
    time.sleep(t)


def click_button(driver, btn_element, t=2):
    # Cliks the button btnElement and waits t seconds
    driver.execute_script("arguments[0].click();", btn_element)
    time.sleep(t)


def expand_section(section, t=4):
    # Expands a section from: ("https://www.electrocosto.com/" + section) to show all products in this section
    url = "https://www.electrocosto.com/" + section

    # Starting selenium webdriver
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(t)

    # Get class w-100, where the scroller observer is
    w_100_element = driver.find_element(By.CLASS_NAME, 'w-100')

    # Loop until button (3 scrolls and the button appears)
    for index in range(3):
        scroll_to(driver, w_100_element)
    time.sleep(t)

    # Get and click the button 'Mostras más productos'
    btn_primary_element = w_100_element.find_element(By.CLASS_NAME, 'btn.btn-primary')
    click_button(driver, btn_primary_element)
    time.sleep(t)

    # Set a stop number of times we scroll and the number of items don't increase
    scroll_limit = 5
    not_increase_count = 0
    n_items = len(driver.find_elements(By.CLASS_NAME, 'recomender-block-item'))

    # Start scrolling loop until limit was reach
    while not_increase_count < scroll_limit:
        scroll_to(driver, w_100_element)
        new_n_items = len(driver.find_elements(By.CLASS_NAME, 'recomender-block-item'))
        print(new_n_items)
        if n_items == new_n_items:
            not_increase_count += 1
        else:
            not_increase_count = 0
            n_items = new_n_items

    return driver.page_source
