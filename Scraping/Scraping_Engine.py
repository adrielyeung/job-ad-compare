# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import pandas as pd
import requests
import unicodedata

# Function declarations
def set_up_headless_driver():
    # Headless option meaning not show browser window
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    DRIVER_PATH = 'C:\\Users\\Adriel\\Downloads\\chromedriver_win32\\chromedriver'
    # driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    return webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

def find_all_by(upper_level_object, extraction_level):
    if row['{}_attribute'.format(extraction_level)] == "id":
        if len(upper_level_object.find_all(row['{}_name'.format(extraction_level)], id=row['{}_tag'.format(extraction_level)])) > 0:
            return upper_level_object.find_all(row['{}_name'.format(extraction_level)], id=row['{}_tag'.format(extraction_level)])[row['{}_item'.format(extraction_level)]]
    elif row['{}_attribute'.format(extraction_level)] == "class":
        if len(upper_level_object.find_all(row['{}_name'.format(extraction_level)], class_=row['{}_tag'.format(extraction_level)])) > 0:
            return upper_level_object.find_all(row['{}_name'.format(extraction_level)], class_=row['{}_tag'.format(extraction_level)])[row['{}_item'.format(extraction_level)]]
    elif row['{}_attribute'.format(extraction_level)] == "none":
        if len(upper_level_object.find_all(row['{}_name'.format(extraction_level)])) > 0:
            return upper_level_object.find_all(row['{}_name'.format(extraction_level)])[int(row['{}_item'.format(extraction_level)])]
    elif row['{}_attribute'.format(extraction_level)] == "self":
        return upper_level_object
    return None

def print_format_unicode(heading, bs_object, normal_form="NFKC"):
    if not bs_object is None:
        print(heading + unicodedata.normalize(normal_form, bs_object.text.strip()))
    else:
        print(heading + 'Not found')

job_ad_sites = pd.read_csv('job_ad_sites.csv')
job_ad_sites.fillna(-999999, inplace=True)
job_ad_sites.Result_item = job_ad_sites.Result_item.astype(int)
job_ad_sites.Title_item = job_ad_sites.Title_item.astype(int)
job_ad_sites.Company_item = job_ad_sites.Company_item.astype(int)
job_ad_sites.Location_item = job_ad_sites.Location_item.astype(int)
job_ad_sites.Description_item = job_ad_sites.Description_item.astype(int)
job_ad_sites.URL_item = job_ad_sites.URL_item.astype(int)

current_datetime = datetime.now()
driver = set_up_headless_driver()
# Store stdout as object (restore later)
stdout_obj = sys.stdout
with open("JobReport_" + current_datetime.strftime("%Y%m%d_%H%M%S") + ".txt", "w", encoding = 'utf-8') as report_file:
    # Set everything printed to stdout to file instead
    sys.stdout = report_file
    print("Job Report on " + current_datetime.strftime("%d/%m/%Y %H:%M:%S"))
    print("=================================")
    for index, row in job_ad_sites.iterrows():
        page = requests.get(row['Listing_URL'])
        soup = BeautifulSoup(page.content, 'html.parser')
        results = find_all_by(soup, 'Result')
        job_elems = results.find_all(row['Element_name'], class_=row['Element_tag'])
        
        for job_elem in job_elems:
            description_elem = None
            content = None
            title_elem = find_all_by(job_elem, 'Title')
            company_elem = find_all_by(job_elem, 'Company')
            location_elem = find_all_by(job_elem, 'Location')
            URL = find_all_by(job_elem, 'URL')

            if not any((title_elem, company_elem, location_elem, URL)):
                continue

            URL = URL['href']

            if str.startswith(URL, '/'):
                URL = row['Prefix_URL'] + URL

            try:
                page_content = driver.get(URL)
                if row['Description_attribute'] == 'id':
                    content = driver.find_element_by_id(row['Description_tag'])
                elif row['Description_attribute'] == 'class':
                    content = driver.find_element_by_class_name(row['Description_tag'])
                if not content is None:
                    description_elem = content.text
            except KeyError:
                continue
            print('Source: ' + row['Site'])
            print_format_unicode('Title: ', title_elem)
            print_format_unicode('Company: ', company_elem)
            print_format_unicode('Location: ', location_elem)
            if not description_elem is None:
                print()
                print('Description')
                print('===========')
                print(description_elem)
                print()
            else:
                print('Description: Not found')
            print("Link: " + unicodedata.normalize("NFKC", URL))
            print('=======================================================================================================================================================')
            print()

driver.quit()
# Restore stdout
sys.stdout = stdout_obj
print("Finished successfully")
