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
        self._first_page_title_list = []
        self._first_page_company_list = []
        self._previous_page_title_list = []
        self._previous_page_company_list = []
    
    def scrape_all(self):
        '''
        Scrape all sites in the config file (data).
        '''
        if not hasattr(self, '_driver'):
            self._driver = self._set_up_headless_driver()
        for index, row in self._data.iterrows():
            # Lists below are for checking when any repetitions occur, which means to stop scraping
            # List of job titles of first page scraped
            self._first_page_title_list = []
            self._first_page_company_list = []
            # List of job titles of previous page scraped
            self._previous_page_title_list = []
            self._previous_page_company_list = []
            scrape_finish = False
            
            page_num = int(row['Page_num_start'])
            while not scrape_finish:
                scrape_finish = self.scrape(row, page_num)
                page_num += int(row['Page_num_increment'])
    
    def scrape(self, row, page_num=1):
        '''
        Scrape site for HTML tags as described in row self._row in the Pandas dataframe.
        
        Parameters
        ----------
        row : pandas.Series
            A row of config data, contains info of 1 website for scraping
        page_num : int, default 1
            Page number to scrape (if the site supports page toggling via page number)
        '''
        self._row = row
        if len(self._first_page_title_list) == 0:
            first_page = True
        else:
            first_page = False
        
        separator = self._row['Search_keyword_separator']
        category_URL = self._convert_to_URL(self.category, separator)
        location_URL = self._convert_to_URL(self.location, separator)
        
        # Check if website supports toggling page number
        if '{page_num}' in self._row['Listing_URL']:
            toggle_page = True
        else:
            toggle_page = False
        
        fetch_URL = self._row['Listing_URL'].format(job_query=category_URL, location_query=location_URL, page_num=page_num, previous_page_num=page_num-1)
        print(fetch_URL)
        page = requests.get(fetch_URL)
        # Check for redirections -> this means the page number does not exist
        if toggle_page and len(page.history) > 0:
            return True
        soup = BeautifulSoup(page.content, 'html.parser')
        if soup is not None:
            results = self._element_finder.find_item_by(self._row, soup, 'Result')
            
            if results is not None:
                job_elems = self._element_finder.find_all_by(self._row, results, 'Element')
                checked_stop = False
        
                for job_elem in job_elems:
                    content = None
                    title_elem = self._element_finder.find_item_by(self._row, job_elem, 'Title')
                    company_elem = self._element_finder.find_item_by(self._row, job_elem, 'Company')
                    location_elem = self._element_finder.find_item_by(self._row, job_elem, 'Location')
                    URL = self._element_finder.find_item_by(self._row, job_elem, 'URL')
                    
                    if not any((title_elem, company_elem, location_elem, URL)):
                        continue
                    
                    URL = URL['href']
                    
                    # Compare job result with first page and previous page to see if any redirections have occured
                    # Compare job title and company
                    # If yes, scraping is finished and should stop
                    if not first_page and not checked_stop:
                        for index in (i for i, e in enumerate(self._first_page_title_list) if e == self._print_format_unicode(title_elem)):
                            if self._first_page_company_list[index] == self._print_format_unicode(company_elem):
                                print("Stopped match with first page job " + self._print_format_unicode(title_elem) + " " + self._print_format_unicode(company_elem))
                                return True
                            
                        for index in (i for i, e in enumerate(self._previous_page_title_list) if e == self._print_format_unicode(title_elem)):
                            if self._previous_page_company_list[index] == self._print_format_unicode(company_elem):
                                print("Stopped match with previous page job " + self._print_format_unicode(title_elem) + " " + self._print_format_unicode(company_elem))
                                return True
                        
                    self._previous_page_title_list = []
                    self._previous_page_company_list = []
        
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
                    if first_page:
                        self._first_page_title_list.append(self._print_format_unicode(title_elem))
                    self._previous_page_title_list.append(self._print_format_unicode(title_elem))
                    
                    self.company_list.append('Company: ' + self._print_format_unicode(company_elem))
                    if first_page:
                        self._first_page_company_list.append(self._print_format_unicode(company_elem))
                    self._previous_page_company_list.append(self._print_format_unicode(company_elem))
                    
                    self.location_list.append('Location: ' + self._print_format_unicode(location_elem))
                    self.site_list.append('Source: ' + self._row['Site'] + '\n')
                    self.link_list.append('Link: ' + URL + '\n')
                    
                    checked_stop = True
                    
        if toggle_page and len(self._previous_page_title_list) > 0:
            return False
        else:
            print("Stopped no more job")
            return True
    
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
