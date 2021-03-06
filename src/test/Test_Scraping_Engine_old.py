# -*- coding: utf-8 -*
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unicodedata
import src.Scraping_Engine_old as se
from src.__init__ import get_root_path
import pandas as pd

class Test_Scraping_Engine_old(unittest.TestCase):
    
    DRIVER_PATH = 'C:\\Users\\Adriel\\Downloads\\chromedriver_win32\\chromedriver'
    TEST_STRING = 'Hello World'
    TEST_CATEGORY = 'Test category'
    TEST_LOCATION = 'Location'
    
    @patch('pandas.DataFrame')
    def setUp(self, mock_dataframe):
        self.test_scraping_engine = se.Scraping_Engine(pd.read_csv(get_root_path() + 'Config\\job_ad_sites_old.csv'), self.TEST_CATEGORY, self.TEST_LOCATION)
    
    def test__set_up_headless_driver(self):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        expected_driver = webdriver.Chrome(options=options, executable_path=self.DRIVER_PATH)
        
        actual_driver = self.test_scraping_engine._set_up_headless_driver()
        self.assertIsInstance(actual_driver, type(expected_driver))
    
    @patch('selenium.webdriver.chrome.webdriver.WebDriver')
    @patch('bs4.element.Tag')
    @patch('src.Element_Finder_old.Element_Finder')
    @patch('requests.get')
    def test_scrape_all(self, mock_get_requests, mock_element_finder, mock_tag, mock_driver):
        mock_content = MagicMock(content='')
        mock_get_requests.return_value = mock_content
        mock_tag = MagicMock(text = self.TEST_STRING)
        mock_element_finder.find_all_by.return_value = [mock_tag]
        mock_element_finder.find_item_by.return_value = mock_tag
        self.test_scraping_engine._element_finder = mock_element_finder
        mock_driver.find_element_by_id.return_value = mock_tag
        self.test_scraping_engine._driver = mock_driver
        mock_tag.__getitem__.return_value = self.TEST_STRING
        self.test_scraping_engine.category = self.TEST_CATEGORY
        self.test_scraping_engine.location = self.TEST_LOCATION
        
        self.test_scraping_engine.scrape_all()
        
        self.assertNotEqual([], self.test_scraping_engine.title_list)
        self.assertNotEqual([], self.test_scraping_engine.company_list)
        self.assertNotEqual([], self.test_scraping_engine.location_list)
    
    @patch('selenium.webdriver.chrome.webdriver.WebDriver')
    @patch('bs4.element.Tag')
    @patch('src.Element_Finder_old.Element_Finder')
    @patch('pandas.Series')
    @patch('requests.get')
    def test_scrape(self, mock_get_requests, mock_row, mock_element_finder, mock_tag, mock_driver):
        mock_content = MagicMock(content='')
        mock_get_requests.return_value = mock_content
        mock_tag = MagicMock(text = self.TEST_STRING)
        mock_element_finder.find_all_by.return_value = [mock_tag]
        mock_element_finder.find_item_by.return_value = mock_tag
        self.test_scraping_engine._element_finder = mock_element_finder
        mock_driver.find_element_by_id.return_value = mock_tag
        self.test_scraping_engine._driver = mock_driver
        mock_tag.__getitem__.return_value = self.TEST_STRING
        mock_row.__getitem__.return_value = 'id'
        
        self.test_scraping_engine.scrape(mock_row)
        
        self.assertNotEqual([], self.test_scraping_engine.title_list)
        self.assertNotEqual([], self.test_scraping_engine.company_list)
        self.assertNotEqual([], self.test_scraping_engine.location_list)
        
            
    @patch('bs4.element.Tag')
    def test__print_format_unicode_valid_string(self, mock_tag):
        mock_tag = MagicMock(text=self.TEST_STRING)
        mock_tag.get_text.return_value = self.TEST_STRING
        actual_string = self.test_scraping_engine._print_format_unicode(mock_tag)
        expected_string = unicodedata.normalize('NFKC', self.TEST_STRING.strip()) + '\n'
        
        self.assertEqual(expected_string, actual_string)
    
    def test__print_format_unicode_invalid_string(self):
        actual_string = self.test_scraping_engine._print_format_unicode(None)
        expected_string = 'Not found\n'
        
        self.assertEqual(expected_string, actual_string)
    
if __name__ == '__main__':
    unittest.main()
