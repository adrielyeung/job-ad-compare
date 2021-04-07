# -*- coding: utf-8 -*
import unittest
from unittest.mock import patch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import src.Scraping_Engine as se
from src.__init__ import get_root_path
import pandas as pd

class Test_Scraping_Engine(unittest.TestCase):
    
    DRIVER_PATH = 'C:\\Users\\Adriel\\Downloads\\chromedriver_win32\\chromedriver'
    TEST_STRING = 'Hello World'
    TEST_CATEGORY = 'Test category'
    TEST_LOCATION = 'Location'
    
    def setUp(self):
        self.test_scraping_engine = se.Scraping_Engine(pd.read_csv(get_root_path() + 'Config\\job_ad_sites.csv'), self.TEST_CATEGORY, self.TEST_LOCATION)
    
    def test__set_up_headless_driver(self):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        expected_driver = webdriver.Chrome(options=options, executable_path=self.DRIVER_PATH)
        
        actual_driver = self.test_scraping_engine._set_up_headless_driver()
        self.assertIsInstance(actual_driver, type(expected_driver))
    
    @patch('selenium.webdriver.chrome.webdriver.WebDriver')
    @patch('pandas.Series')
    def test_scrape_all(self, mock_element, mock_driver):
        mock_driver.find_element_by_xpath.return_value = mock_element
        self.test_scraping_engine._driver = mock_driver
        self.test_scraping_engine._driver_desc = mock_driver
        self.test_scraping_engine.category = self.TEST_CATEGORY
        self.test_scraping_engine.location = self.TEST_LOCATION
        mock_element.__getitem__.return_value = self.TEST_STRING
        
        self.test_scraping_engine.scrape_all()
        
        self.assertNotEqual([], self.test_scraping_engine.title_list)
        self.assertNotEqual([], self.test_scraping_engine.company_list)
        self.assertNotEqual([], self.test_scraping_engine.location_list)
    
    @patch('selenium.webdriver.chrome.webdriver.WebDriver')
    @patch('selenium.webdriver.remote.webelement.WebElement')
    @patch('pandas.Series')
    def test_scrape(self, mock_row, mock_element, mock_driver):
        mock_driver.find_element_by_xpath.return_value = mock_element
        self.test_scraping_engine._driver = mock_driver
        self.test_scraping_engine._driver_desc = mock_driver
        mock_element.__getitem__.return_value = self.TEST_STRING
        mock_row.__getitem__.return_value = '5'
        
        self.test_scraping_engine.scrape(mock_row, self.TEST_CATEGORY, self.TEST_LOCATION)
        
        self.assertNotEqual([], self.test_scraping_engine.title_list)
        self.assertNotEqual([], self.test_scraping_engine.company_list)
        self.assertNotEqual([], self.test_scraping_engine.location_list)
        
if __name__ == '__main__':
    unittest.main()
