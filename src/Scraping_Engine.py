# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import re
import time

class Scraping_Engine:
    DRIVER_PATH = 'C:\\Users\\Adriel\\Downloads\\chromedriver_win32\\chromedriver'
    NEWLINE = '\n'
    NOT_FOUND = 'Not found'
    TITLE = 'Title: '
    COMPANY = 'Company: '
    LOCATION = 'Location: '
    LINK = 'Link: '
    DESCRIPTION = 'Description'
    SKILLS = 'Skills'
    SOURCE = 'Source: '
    UNDERLINE = '='
    
    def __init__(self, data, category, location, excel=False):
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
        self._max_repeats_allowed = 2
        self._excel = excel
        self.site_list = []
        self.title_list = []
        self.company_list = []
        self.location_list = []
        self.description_list = []
        self.skills_list = []
        self.link_list = []
        self._first_page_title_list = []
        self._first_page_company_list = []
        self._previous_page_title_list = [[], []]
        self._previous_page_company_list = [[], []]
    
    def scrape_all(self):
        '''
        Scrape all sites in the config file (data).
        '''
        if not hasattr(self, '_driver'):
            self._driver = self._set_up_headless_driver()
        if not hasattr(self, '_driver_desc'):
            self._driver_desc = self._set_up_headless_driver()
        for index, row in self._data.iterrows():
            # Lists below are for checking when any repetitions occur, which means to stop scraping
            # List of job titles of first page scraped
            self._first_page_title_list = []
            self._first_page_company_list = []
            # List of job titles of previous page scraped (2 lists because one list used for compare, other used to append current page)
            self._previous_page_title_list = [[], []]
            self._previous_page_company_list = [[], []]
            
            separator = row['Search_keyword_separator']
            category_URL = self._convert_to_URL(self.category, separator)
            location_URL = self._convert_to_URL(self.location, separator)
            scrape_finish = False
            
            page_id = int(row['Page_num_start'])
            previous_page_list_use = 0
            while not scrape_finish:
                self._previous_page_title_list[previous_page_list_use] = []
                self._previous_page_company_list[previous_page_list_use] = []
                scrape_finish = self.scrape(row, category_URL, location_URL, page_id, previous_page_list_use)
                page_id += int(row['Page_num_increment'])
                previous_page_list_use = 1 - previous_page_list_use
        self._driver.quit()
        self._driver_desc.quit()
    
    def scrape(self, row, category_URL, location_URL, page_id=1, previous_page_list_use=1):
        '''
        Scrape site for HTML tags as described in row self._row in the Pandas dataframe.
        
        Parameters
        ----------
        row : pandas.Series
            A row of config data, contains info of 1 website for scraping
        category_URL : string
            Job category formatted into URL, with spaces replaced by separator
        location_URL : string
            Location formatted into URL, with spaces replaced by separator
        page_id : int, default 1
            Page number to scrape (if the site supports page toggling via page number)
        previous_page_list_use : int, default 1
            Sublist index (0 or 1) for previous page lists to use. Toggle for each page scraped.
        '''
        def _check_element_exist(element, driver):
            try:
                driver.find_element_by_xpath(element)
            except NoSuchElementException:
                return False
            return True
        
        def _title_or_company_changed():
            return ((title_elem != self._driver.find_element_by_xpath(self._row['Title_tag'].format(result_id=str(rid))).text)
                    or (company_elem != self._driver.find_element_by_xpath(self._row['Company_tag'].format(result_id=str(rid))).text))
        
        def _click_element():
            click_retries = 0
            try:
                self._driver.find_element_by_xpath(self._row['URL_tag'].format(result_id=str(rid))).click()
            except NoSuchElementException:
                return -1
            # Retry clicking element in case failed (no response)
            while click_retries < 5:
                try:
                    self._driver.find_element_by_xpath(self._row['URL_tag'].format(result_id=str(rid))).click()
                except NoSuchElementException:
                    return -1
                if self._wait_for(_title_or_company_changed, 0.5, 2, False):
                    return 0
                click_retries += 1
            return 1
        
        def _find_element(element_name, driver, text=True):
            if self._row['{}_tag'.format(element_name)]:
                try:
                    web_element = driver.find_element_by_xpath(self._row['{}_tag'.format(element_name)].format(result_id=str(rid)))
                    if text:
                        return web_element.text
                    else:
                        return web_element
                except (KeyError, NoSuchElementException):
                    return None
            return None
        
        self._row = row
        if len(self._first_page_title_list) == 0:
            first_page = True
        else:
            first_page = False
        
        # Check if website supports toggling page number
        if '{page_id}' in self._row['Listing_URL']:
            toggle_page = True
        else:
            toggle_page = False
        
        fetch_URL = self._row['Listing_URL'].format(job_query=category_URL, location_query=location_URL, page_id=page_id, previous_page_id=page_id-1)
        self._driver.get(fetch_URL)
        # Wait for element to appear
        result_start = int(self._row['Result_start'])
        result_end = int(self._row['Result_end'])
        result_step = int(self._row['Result_step'])
        if self._row['Description_format'] != "URL":
            if not (self._wait_for(_check_element_exist, 5, 30, True, self._row['URL_tag'].format(result_id=str(result_start)), self._driver)
                or self._wait_for(_check_element_exist, 5, 30, True, self._row['URL_tag'].format(result_id=str(result_start + result_step)), self._driver)):
                return True
        else:
            if not (self._wait_for(_check_element_exist, 5, 30, True, self._row['Title_tag'].format(result_id=str(result_start)), self._driver)
                    or self._wait_for(_check_element_exist, 5, 30, True, self._row['Title_tag'].format(result_id=str(result_start + result_step)), self._driver)):
                return True
        
        # Check for redirections -> this means the page number does not exist
        if toggle_page and self._driver.current_url != fetch_URL:
            return True
        
        repeats = 0
        
        for rid in np.arange(result_start, result_end + result_step, result_step):
            title_elem = None
            company_elem = None
            location_elem = None
            URL = None
            checked_stop = False
            
            if self._row['Description_format'] != "URL":
                click_return = _click_element()
                if click_return == -1:
                    break
                elif click_return == 1:
                    continue
                
            title_elem = _find_element("Title", self._driver)
            company_elem = _find_element("Company", self._driver)
            location_elem = _find_element("Location", self._driver)
            if self._row['Description_format'] == "URL":
                URL = _find_element("URL", self._driver, text=False)
                if URL:
                    URL = URL.get_attribute('href')
                
            if not any((title_elem, company_elem, location_elem, URL)):
                continue
                        
            # Compare job result with first page and previous page to see if any redirections have occured
            # Compare job title and company
            # If 2 time matches, scraping is finished and should stop
            if not first_page and not checked_stop:
                for index in (i for i, e in enumerate(self._first_page_title_list) if e == title_elem):
                    if self._first_page_company_list[index] == company_elem:
                        repeats += 1
                        if repeats > self._max_repeats_allowed:
                            return True
                
                # 1 - previous_page_list_use used to determine which list contains previous page entries
                for index in (i for i, e in enumerate(self._previous_page_title_list[1-previous_page_list_use]) if e == title_elem):
                    if self._previous_page_company_list[1-previous_page_list_use][index] == company_elem:
                        repeats += 1
                        if repeats > self._max_repeats_allowed:
                            return True
            
            if self._row['Description_format'] == "URL":
                if URL:
                    if str.startswith(URL, '/'):
                        URL = self._row['Prefix_URL'] + URL
                
                    self._driver_desc.get(URL)
                    if not self._wait_for(_check_element_exist, 5, 30, True, self._row['Description_tag'], self._driver_desc):
                        return True
                    description_elem = _find_element("Description", self._driver_desc)
                    skills_elem = _find_element("Skills", self._driver_desc)
                else:
                    description_elem = None
                    skills_elem = None
            # Click within dashboard to load job details
            else:
                description_elem = _find_element("Description", self._driver)
                skills_elem = _find_element("Skills", self._driver)
                self.link_list.append('')
            
            if self._excel:
                self._write_to_excel_lists(title_elem, company_elem, location_elem, URL, description_elem, skills_elem, first_page, previous_page_list_use)
            else:
                self._write_to_text_lists(title_elem, company_elem, location_elem, URL, description_elem, skills_elem, first_page, previous_page_list_use)
            
            checked_stop = True
                    
        if toggle_page and len(self._previous_page_title_list[previous_page_list_use]) > 0:
            return False
        else:
            return True
            
    def _write_to_excel_lists(self, title_elem, company_elem, location_elem, URL, description_elem, skills_elem, first_page, previous_page_list_use):
        '''
        Appends the scraped output to the corresponding lists, adding descriptions for a text report and no extra descriptions for an Excel report.

        Parameters
        ----------
        title_elem : string
            Title.
        company_elem : string
            Company.
        location_elem : string
            Location.
        URL : string
            URL.
        description_elem : string
            Job description.
        skills_elem : string
            Job skills.
        first_page : boolean
            Whether the scraped page is the first page.
        previous_page_list_use : int (0/1)
            Which sublist of previous page title/company list to be used by this page.
        '''
        if title_elem:
            self.title_list.append(title_elem)
            if first_page:
                self._first_page_title_list.append(title_elem)
            self._previous_page_title_list[previous_page_list_use].append(title_elem)
        else:
            self.title_list.append(self.NOT_FOUND)
        
        if company_elem:
            self.company_list.append(company_elem)
            if first_page:
                self._first_page_company_list.append(company_elem)
            self._previous_page_company_list[previous_page_list_use].append(company_elem)
        else:
            self.company_list.append(self.NOT_FOUND)
                    
        if location_elem:
            self.location_list.append(location_elem)
        else:
            self.location_list.append(self.NOT_FOUND)
            
        if URL:
            self.link_list.append(URL)
        else:
            self.link_list.append(self.NOT_FOUND)
        
        if description_elem:
            self.description_list.append(description_elem)
        else:
            self.description_list.append(self.NOT_FOUND)
            
        if skills_elem:
            self.skills_list.append(skills_elem)
        else:
            self.skills_list.append(self.NOT_FOUND)
            
        self.site_list.append(self._row['Site'])
    
    def _write_to_text_lists(self, title_elem, company_elem, location_elem, URL, description_elem, skills_elem, first_page, previous_page_list_use):
        '''
        Appends the scraped output to the corresponding lists, adding descriptions for a text report and no extra descriptions for an Excel report.

        Parameters
        ----------
        title_elem : string
            Title.
        company_elem : string
            Company.
        location_elem : string
            Location.
        URL : string
            URL.
        description_elem : string
            Job description.
        skills_elem : string
            Job skills.
        first_page : boolean
            Whether the scraped page is the first page.
        previous_page_list_use : int (0/1)
            Which sublist of previous page title/company list to be used by this page.
        '''
        if title_elem:
            self.title_list.append(self.TITLE + title_elem + self.NEWLINE)
            if first_page:
                self._first_page_title_list.append(title_elem)
            self._previous_page_title_list[previous_page_list_use].append(title_elem)
        else:
            self.title_list.append(self.TITLE + self.NOT_FOUND + self.NEWLINE)
        
        if company_elem:
            self.company_list.append(self.COMPANY + company_elem + self.NEWLINE)
            if first_page:
                self._first_page_company_list.append(company_elem)
            self._previous_page_company_list[previous_page_list_use].append(company_elem)
        else:
            self.company_list.append(self.COMPANY + self.NOT_FOUND + self.NEWLINE)
                    
        if location_elem:
            self.location_list.append(self.LOCATION + location_elem + self.NEWLINE)
        else:
            self.location_list.append(self.LOCATION + self.NOT_FOUND + self.NEWLINE)
            
        if URL:
            self.link_list.append(self.LINK + URL + self.NEWLINE)
        else:
            self.link_list.append(self.LINK + self.NOT_FOUND + self.NEWLINE)
        
        if description_elem:
            self.description_list.append(self.NEWLINE + self.DESCRIPTION + self.NEWLINE + self.UNDERLINE * len(self.DESCRIPTION) + self.NEWLINE 
                                         + description_elem + self.NEWLINE)
        else:
            self.description_list.append(self.NEWLINE + self.DESCRIPTION + self.NEWLINE + self.UNDERLINE * len(self.DESCRIPTION) + self.NEWLINE 
                                         + self.NOT_FOUND + self.NEWLINE)
            
        if skills_elem:
            self.skills_list.append(self.NEWLINE + self.SKILLS + self.NEWLINE + self.UNDERLINE * len(self.SKILLS) + self.NEWLINE 
                                         + skills_elem + self.NEWLINE)
        else:
            self.skills_list.append(self.NEWLINE + self.SKILLS + self.NEWLINE + self.UNDERLINE * len(self.SKILLS) + self.NEWLINE 
                                         + self.NOT_FOUND + self.NEWLINE)
            
        self.site_list.append(self.SOURCE + self._row['Site'] + self.NEWLINE)
    
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
    
    def _wait_for(self, condition, wait_interval, max_wait_time, force_wait, *args):
        '''
        Helper function to sleep execution for wait_interval-second intervals until condition is met or after max_wait_time seconds.

        Parameters
        ----------
        condition : function which returns a boolean
            Boolean condition function, if satisfied, will stop sleeping. Called to check every wait_interval seconds.
        wait_interval : int or float
            Interval between each check of condition (in sec).
        max_wait_time : int or float
            Maximum time to wait for before exiting (in sec).
        force_wait : boolean
            Whether to force wait for wait_interval before checking. This time does not count toward max_wait_time.
        *args : objects
            Additional arguments to call the condition function.
            
        Returns
        -------
        True is condition is met or False if 30 secs has passed without meeting the condition.
        '''
        if force_wait:
            time.sleep(wait_interval)
        start_time = time.time()
        while (not condition(*args)) and (time.time() < start_time + max_wait_time):
            time.sleep(wait_interval)
        if condition(*args):
            return True
        else:
            return False
    