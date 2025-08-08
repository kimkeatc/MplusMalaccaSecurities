#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Import standard libraries
import logging
import pandas
import time

# Import third-party libraries
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver


class UIHandler:

    def __init__(self):
        self.webdriver = webdriver.Chrome()
        self.cookies = []

    def harvest_stockcodes(self, stockcodes: list = [], timeout: int = 10, offline_mode: bool = False):

        if self.cookies == []:
            self.cookies = self.webdriver.get_cookies()

        self.webdriver.switch_to.default_content()
        # Waiting the table to be loaded
        if offline_mode is False:
            while not WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.frame_to_be_available_and_switch_to_it(locator=(By.ID, "ifrMP"))):
                pass
            while not WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.frame_to_be_available_and_switch_to_it(locator=(By.ID, "ifrm"))):
                pass

        results = {}
        length_stockcodes = len(stockcodes)
        for index, stockcode in enumerate(stockcodes, start=1):
            logging.info(f"Processing stock code {index:03d}/{length_stockcodes:03d} - {stockcode}")
            row_index = self._search_stockcode(stockcode)

            dates_selection = Select(webelement=WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.CLASS_NAME, "ui-sti-sel"))))
            dates = [s.get_attribute("value") for s in dates_selection.options]
            for date in dates:
                dates_selection.select_by_value(value=date)
                overall = self._get_spOaStk()
                all_transactions = self._get_spAllTrx()
                grouped_by_time = self._get_spGrpByTm()
                grouped_by_price, grouped_by_volume = self._get_spGrpByPx()
                results.setdefault(stockcode, {}).setdefault(date, (overall, all_transactions, grouped_by_time, grouped_by_price, grouped_by_volume))
                break

            # Reset to home
            WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.CLASS_NAME, "ui-icon-home"))).click()

            if offline_mode is False:

                # Right click on stockcode row
                ActionChains(driver=self.webdriver).context_click(on_element=self.webdriver.find_element(by=By.XPATH, value=f"/html/body/form/div[3]/div[2]/div[5]/div/div[3]/div[5]/div/table/tbody/tr[2]/td[{row_index}]")).perform()
                # WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.frame_to_be_available_and_switch_to_it(locator=(By.ID, "jqCtxtMn")))

                # Right click on "Fundanmental Analysis"
                self.webdriver.find_element(by=By.XPATH, value="/html/body/div[2]/ul/li[11]").click()

                self.webdriver.switch_to.window(window_name=self.webdriver.window_handles[1])
                session_id = WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.NAME, "CNID"))).get_attribute("value")
                logging.info(f"https://mplus.equitiestracker.com/snapshot.php?stk={stockcode}&session_id={session_id}")
                while not WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.frame_to_be_available_and_switch_to_it(locator=(By.ID, "ChartFrame"))):
                    pass

                snapshot = WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.XPATH, "/html/body/div[3]/div/ul/li[1]/a"))).text
                logging.info(snapshot)

        return results

    def _search_stockcode(self, stockcode: str, timeout: int = 10) -> int:
        WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.CLASS_NAME, "ui-search-input-custom"))).send_keys(stockcode)
        WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.CLASS_NAME, "ui-icon-search"))).click()
        for index, row in enumerate(self.webdriver.find_element(by=By.XPATH, value="/html/body/form/div[3]/div[2]/div[5]/div/div[3]/div[5]/div/table").find_elements(by=By.TAG_NAME, value="tr")):
            if row.find_elements(by=By.TAG_NAME, value="td")[0].text == stockcode:
                ActionChains(driver=self.webdriver).double_click(on_element=self.webdriver.find_element(by=By.XPATH, value=f"/html/body/form/div[3]/div[2]/div[5]/div/div[3]/div[5]/div/table/tbody/tr[2]/td[{index}]")).perform()
                return index

    def _get_spOaStk(self, timeout: int = 10) -> pandas.DataFrame:
        ActionChains(driver=self.webdriver).double_click(on_element=self.webdriver.find_element(by=By.ID, value="spOaStk")).perform()
        dataframe = pandas.read_html(io=WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.XPATH, "/html/body/form/div[3]/div[2]/div[5]/div/div[3]/div[3]/div[2]/div[1]/div[2]/table"))).get_attribute("outerHTML"))[0]
        dataframe.columns = dataframe.iloc[1]
        dataframe = dataframe[2:]
        return dataframe

    def _get_spAllTrx(self, timeout: int = 10) -> pandas.DataFrame:
        ActionChains(driver=self.webdriver).double_click(on_element=self.webdriver.find_element(by=By.ID, value="spAllTrx")).perform()

        # Get the row number
        while True:
            rows = WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.XPATH, "/html/body/form/div[3]/div[2]/div[5]/div/div[3]/div[3]/div[2]/div[2]/table/tbody/tr[1]/td[1]"))).text
            if rows:
                break

        # Scroll the table
        for _ in range(int(rows) // 100):
            self.webdriver.execute_script("arguments[0].scrollTop += 10000;", self.webdriver.find_element(by=By.CLASS_NAME, value="ui-sti-alltrx-cntnr"))
            time.sleep(0.5)

        dataframe = pandas.read_html(io=WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.ID, "tblAllTrx"))).get_attribute("outerHTML"))[0]
        return dataframe

    def _get_spGrpByTm(self, timeout: int = 10) -> pandas.DataFrame:
        ActionChains(driver=self.webdriver).double_click(on_element=self.webdriver.find_element(by=By.ID, value="spGrpByTm")).perform()
        dataframe = pandas.read_html(io=WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.ID, "tblGbt"))).get_attribute("outerHTML"))[0]
        return dataframe

    def _get_spGrpByPx(self, timeout: int = 10) -> pandas.DataFrame:
        ActionChains(driver=self.webdriver).double_click(on_element=self.webdriver.find_element(by=By.ID, value="spGrpByPx")).perform()
        dataframe_tblPx = pandas.read_html(io=WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.ID, "tblPx"))).get_attribute("outerHTML"))[0]
        dataframe_tblVolt = pandas.read_html(io=WebDriverWait(driver=self.webdriver, timeout=timeout).until(method=expected_conditions.presence_of_element_located(locator=(By.ID, "tblVolt"))).get_attribute("outerHTML"))[0]
        return dataframe_tblPx, dataframe_tblVolt
