#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Import standard libraries
import threading
import logging
import sys

# Import third-party libraries
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# Import custom script
try:
    from ui_handler import UIHandler
    from misc import dec_performance, chunks
except ImportError:
    from .ui_handler import UIHandler
    from .misc import dec_performance, chunks

NUMBER_OF_THREADS = 2


class MPlus(UIHandler):

    def __init__(self):
        super().__init__()
        self.url = "https://www.mplusonline.com.my/wsgCltx/csmsq.aspx"

    def init_dashboard(self, timeout: int = 60):
        self.webdriver.get(url=self.url)
        self.webdriver.maximize_window()

        # Hold for pops out window
        WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.CSS_SELECTOR, "span[class='ui-button-icon ui-icon ui-icon-closethick']")))

        # To close the pops out window
        ActionChains(driver=self.webdriver).click(self.webdriver.find_element(by=By.CSS_SELECTOR, value="span[class='ui-button-icon ui-icon ui-icon-closethick']")).perform()


@dec_performance(log=logging.info)
def mThread_harvest_stockcodes(stockcodes: list[str], number_of_threads: int = NUMBER_OF_THREADS) -> dict:

    length_stockcodes = len(stockcodes)
    logging.info(f"Number of stockcodes that require processing: {length_stockcodes}")
    if length_stockcodes <= number_of_threads:
        number_of_threads = length_stockcodes
    logging.info(f"Number of threads will be allocated: {number_of_threads}")

    threads, results = [], {}
    stockcodes = chunks(iterable=stockcodes, n=number_of_threads)
    for stockcode in stockcodes:
        threads.append(threading.Thread(
            target=sThread_harvest_stockcodes,
            args=[stockcode, results]
        ))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return results


def sThread_harvest_stockcodes(stockcodes: list[str], results: dict = {}) -> dict:

    mplus = MPlus()

    # Initialize dashboard
    mplus.init_dashboard()
    logging.info("Successfully initialize MPLUS dashboard...")

    # Get data
    results.update(mplus.harvest_stockcodes(stockcodes=stockcodes, offline_mode=True))

    # Close webdriver
    mplus.webdriver.quit()

    return results


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

    results = mThread_harvest_stockcodes(stockcodes=["1818", "0138"])
    logging.info(results)
