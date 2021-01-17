# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import src.Element_Finder as ef
import requests
import unicodedata
import re

class Scraping_Engine:
    DRIVER_PATH = 'C:\\Users\\Adriel\\Downloads\\chromedriver_win32\\chromedriver'
    
    def __init__(self, data, category, location):
        '''
        Initialises the scraping engine.

        Parameters
        ----------
        data : Pandas dataframe
            Dataframe of config file (listing of all sites and HTML tags to scrape for).
        
        category : string
            Filter job category read from GUI (input by user).
        
        location : string
            Filter location of job read from GUI (input from user).

        Returns
        -------
        None.
        '''
        self._data = data
        self.category = category
        self.location = location
        self._element_finder = ef.Element_Finder()
        self.site_list = []
        self.title_list = []
        self.company_list = []
        self.location_list = []
        self.description_list = []
        self.link_list = []
    
    def scrape_all(self):
        '''
        Scrape all sites in the config file (data).
        '''
        if not hasattr(self, '_driver'):
            self._driver = self._set_up_headless_driver()
        for index, row in self._data.iterrows():
            self.scrape(row)
    
    def scrape(self, row):
        '''
        Scrape site for HTML tags as described in row self._row in the Pandas dataframe.
        '''
        self._row = row
        separator = self._row['Search_keyword_separator']
        category_URL = self._convert_to_URL(self.category, separator)
        location_URL = self._convert_to_URL(self.location, separator)
        fetch_URL = self._row['Listing_URL'].format(job_query=category_URL, location_query=location_URL)
        page = requests.get(fetch_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = self._element_finder.find_item_by(self._row, soup, 'Result')
        job_elems = self._element_finder.find_all_by(self._row, results, 'Element')
        
        for job_elem in job_elems:
            content = None
            title_elem = self._element_finder.find_item_by(self._row, job_elem, 'Title')
            company_elem = self._element_finder.find_item_by(self._row, job_elem, 'Company')
            location_elem = self._element_finder.find_item_by(self._row, job_elem, 'Location')
            URL = self._element_finder.find_item_by(self._row, job_elem, 'URL')
            
            if not any((title_elem, company_elem, location_elem, URL)):
                continue
            
            URL = URL['href']

            if str.startswith(URL, '/'):
                URL = self._row['Prefix_URL'] + URL
            
            try:
                self._driver.get(URL)
                if self._row['Description_attribute'] == 'id':
                    content = self._driver.find_element_by_id(self._row['Description_tag'])
                elif self._row['Description_attribute'] == 'class':
                    content = self._driver.find_element_by_class_name(self._row['Description_tag'])
                elif self._row['Description_attribute'] == 'xpath':
                    content = self._driver.find_element_by_xpath(self._row['Description_tag'])
                if not content is None:
                    self.description_list.append('\nDescription\n===========\n' + content.text + '\n')
                else:
                    self.description_list.append('\nDescription\n===========\nNot found\n')
            except (KeyError, NoSuchElementException):
                continue
        
            self.title_list.append('Title: ' + self._print_format_unicode(title_elem))
            self.company_list.append('Company: ' + self._print_format_unicode(company_elem))
            self.location_list.append('Location: ' + self._print_format_unicode(location_elem))
            self.site_list.append('Source: ' + self._row['Site'] + '\n')
            self.link_list.append('Link: ' + URL + '\n')
    
    def _set_up_headless_driver(self):
        '''
        Set up a Chrome driver in headless mode (not show browser window).
    
        Returns
        -------
        Chrome web driver.
        '''
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
    
        return webdriver.Chrome(options=options, executable_path=self.DRIVER_PATH)
    
    def _print_format_unicode(self, bs_object, normal_form="NFKC"):
        '''
        Normalise the string into a Unicode normalisation form, and write into report_file.
    
        Parameters
        ----------
        bs_object : bs4.element.Tag
            HTML tag object to extract text from.
        normal_form : string, optional
            Unicode normalisation form. The default is "NFKC".
    
        Returns
        -------
        Normalised string.
        '''
        if not bs_object is None:
            return unicodedata.normalize(normal_form, bs_object.text.strip()) + '\n'
        else:
            return 'Not found\n'
    
    def _convert_to_URL(self, text, separator):
        '''
        Converts a normal human-readable string into a URL-style string, with all spaces replaced by separator.

        Parameters
        ----------
        text : string
            Input text to convert.
        separator : string
            Separator in the URL (e.g. - / +)

        Returns
        -------
        text : string
            Input text with all spaces replaced by separator.

        '''
        text = text.lower()
        text = re.sub('\s+', separator, text)
        return text
