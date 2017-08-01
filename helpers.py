from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


def getChromeDriver():
    chromedriver = "/usr/local/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    chrome_options = Options()
    # This make Chromium reachable
    chrome_options.add_argument("--no-sandbox")
    # Overrides default choices
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-user-media-security=true")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    return webdriver.Chrome(chromedriver, chrome_options=chrome_options)


def setValue(browser, i, j, val):
    # Websudoku has reversed row and col index
    cellId = 'c' + str(j) + str(i)
    cell = browser.find_element_by_id(cellId).find_element_by_tag_name('input')
    browser.execute_script("arguments[0].value = arguments[1]", cell, val)
