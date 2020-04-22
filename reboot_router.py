import socket
import requests
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import platform


logging.basicConfig(filename='router_log.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger().addHandler(logging.StreamHandler())


def launch_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # options.add_argument("--headless")
    exec_path = "chromedriver"
    if platform.system() == 'Linux':
        exec_path = "./chromedriver"
    driver = webdriver.Chrome(executable_path=exec_path, options=options)
    return driver


def login(driver):
    driver.get("http://192.168.0.1/userRpm/LoginRpm.htm?Save=Save")
    user_id = driver.find_element_by_xpath('//input[@id="userName"]')
    user_id.clear()
    user_id.send_keys("admin")

    passwd = driver.find_element_by_xpath('//input[@id="pcPassword"]')
    passwd.clear()
    passwd.send_keys("admin")

    passwd.send_keys(Keys.ENTER)


def reboot_router(driver):

    menu_frame = driver.find_element_by_xpath(
        "//frame[@name='bottomLeftFrame']")
    # navigate to reboot option parent
    for _ in range(17):
        menu_frame.send_keys(Keys.TAB)
    menu_frame.send_keys(Keys.ENTER)

    # navigate to reboot option
    for _ in range(6):
        menu_frame.send_keys(Keys.TAB)
    menu_frame.send_keys(Keys.ENTER)

    # click on reboot & approve alert
    main_frame = driver.find_element_by_xpath("//frame[@name='mainFrame']")
    main_frame.send_keys(Keys.TAB)
    main_frame.send_keys(Keys.ENTER)
    # TODO: check this
    main_frame.send_keys(Keys.ENTER)


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


# if no internet reboot router
if not is_connected():
    driver = launch_browser()
    login(driver)
    reboot_router(driver)
