# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import requests
import unicodedata

class Scraping_Engine:
    DRIVER_PATH = '<set up Chrome web driver path>'
    
    def __init__(self, data):
        '''
        Initialises the scraping engine.

        Parameters
        ----------
        data : Pandas dataframe
            Dataframe of config file (listing of all sites and HTML tags to scrape for).

        Returns
        -------
        None.
        '''
        self._driver = self._set_up_headless_driver()
        self._data = data
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
        for index, row in self._data.iterrows():
            self._row = row
            self.scrape()
    
    def scrape(self):
        '''
        Scrape site for HTML tags as described in row self._row in the Pandas dataframe.
        '''
        page = requests.get(self._row['Listing_URL'])
        soup = BeautifulSoup(page.content, 'html.parser')
        results = self._find_item_by(soup, 'Result')
        job_elems = self._find_all_by(results, 'Element')
        
        for job_elem in job_elems:
            content = None
            title_elem = self._find_item_by(job_elem, 'Title')
            company_elem = self._find_item_by(job_elem, 'Company')
            location_elem = self._find_item_by(job_elem, 'Location')
            URL = self._find_item_by(job_elem, 'URL')

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
    
    def _find_item_by(self, upper_level_object, extraction_level):
        '''
        Find matching HTML element with specified attributes from config file (if 
        >1 matching elements, return the one as specified by 
        <extraction_level>_item in the config file).
    
        Parameters
        ----------
        upper_level_object : bs4.BeautifulSoup or bs4.element.Tag
            The object to look for tags within.
        extraction_level : string
            Extraction level as specified in config (Result / Element / Title / 
            Company / Location / Description / URL).
    
        Returns
        -------
        bs4.element.Tag
            The HTML tag element which matches config values.
            If no match, return None.
        '''
        if self._row['{}_attribute'.format(extraction_level)] == "id":
            if len(upper_level_object.find_all(self._row['{}_name'.format(extraction_level)], id=self._row['{}_tag'.format(extraction_level)])) > 0:
                return upper_level_object.find_all(self._row['{}_name'.format(extraction_level)], id=self._row['{}_tag'.format(extraction_level)])[self._row['{}_item'.format(extraction_level)]]
        elif self._row['{}_attribute'.format(extraction_level)] == "class":
            if len(upper_level_object.find_all(self._row['{}_name'.format(extraction_level)], class_=self._row['{}_tag'.format(extraction_level)])) > 0:
                return upper_level_object.find_all(self._row['{}_name'.format(extraction_level)], class_=self._row['{}_tag'.format(extraction_level)])[self._row['{}_item'.format(extraction_level)]]
        elif self._row['{}_attribute'.format(extraction_level)] == "none":
            if len(upper_level_object.find_all(self._row['{}_name'.format(extraction_level)])) > 0:
                return upper_level_object.find_all(self._row['{}_name'.format(extraction_level)])[int(self._row['{}_item'.format(extraction_level)])]
        elif self._row['{}_attribute'.format(extraction_level)] == "self":
            return upper_level_object
        return None
    
    def _find_all_by(self, upper_level_object, extraction_level):
        '''
        Find all matching HTML element with specified attributes from config file.
    
        Parameters
        ----------
        upper_level_object : bs4.BeautifulSoup or bs4.element.Tag
            The object to look for tags within.
        extraction_level : string
            Extraction level as specified in config (Result / Element / Title / 
            Company / Location / Description / URL).
    
        Returns
        -------
        bs4.element.ResultSet
            The HTML ResultSet which contains all matches.
            If no match, return None.
        '''
        if self._row['{}_attribute'.format(extraction_level)] == "id":
            if len(upper_level_object.find_all(self._row['{}_name'.format(extraction_level)], id=self._row['{}_tag'.format(extraction_level)])) > 0:
                return upper_level_object.find_all(self._row['{}_name'.format(extraction_level)], id=self._row['{}_tag'.format(extraction_level)])
        elif self._row['{}_attribute'.format(extraction_level)] == "class":
            if self._row['Element_item'] == 'sub':
                return upper_level_object.find(self._row['{}_name'.format(extraction_level)], class_=self._row['{}_tag'.format(extraction_level)]).find_all(self._row['{}_name'.format(extraction_level)], recursive=False)
            else:
                return upper_level_object.find_all(self._row['{}_name'.format(extraction_level)], class_=self._row['{}_tag'.format(extraction_level)])
        elif self._row['{}_attribute'.format(extraction_level)] == "none":
            if len(upper_level_object.find_all(self._row['{}_name'.format(extraction_level)])) > 0:
                return upper_level_object.find_all(self._row['{}_name'.format(extraction_level)])
        elif self._row['{}_attribute'.format(extraction_level)] == "self":
            return upper_level_object
        return None
    
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
