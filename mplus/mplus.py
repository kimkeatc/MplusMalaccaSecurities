#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Import standard libraries
import logging
import time
import sys

# Import third-party libraries
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# Import custom script
try:
    from ui_handler import UIHandler
except ImportError:
    from .ui_handler import UIHandler


class MPlus(UIHandler):

    def __init__(self):
        super().__init__()
        self.url = "https://www.mplusonline.com.my/"

    def login(self, username: str, password: str, timeout: int = 10) -> None:
        self.webdriver.get(url=self.url)
        self.webdriver.maximize_window()
        WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.NAME, "txtUserID"))).send_keys(username)
        WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.NAME, "txtPword"))).send_keys(password)
        WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.XPATH, "/html/body/div/section[2]/div/form/div/div[2]/button/span"))).click()
        time.sleep(5)

    def logout(self, timeout: int = 10) -> None:
        self.webdriver.switch_to.window(window_name=self.webdriver.window_handles[0])
        self.webdriver.switch_to.default_content()
        WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.XPATH, "/html/body/div[2]/div/div/div[1]/a/span"))).click()


if __name__ == "__main__":

    # Setup logging
    logger = logging.getLogger(name=None)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(level=logging.INFO)

    # Create a stream handler
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(
        fmt=logging.Formatter(
            fmt="[%(thread)5s] [%(threadName)32s] [%(asctime)s] [%(levelname)8s] : %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(hdlr=stream_handler)

    mplus = MPlus()

    # Login account
    mplus.login(username="", password="")
    logging.info("Successfully login MPLUS...")

    # Get data
    results = mplus.harvest_stockcodes(stockcodes=["1818"])
    logging.info(results)

    # Logout account
    mplus.logout()

    # Close webdriver
    mplus.webdriver.quit()
