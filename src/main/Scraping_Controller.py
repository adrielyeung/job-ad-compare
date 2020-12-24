# -*- coding: utf-8 -*-
import Scraping_Engine as se
import Csv_Reader as cr
import Report_Writer as rw
import Keyword_Extractor as ke
from datetime import datetime
    
def main():
    current_datetime = datetime.now()
    CONFIG_PATH = 'C:\\Users\\Adriel\\Documents\\Python Scripts\\Scraping\\Config\\job_ad_sites.csv'
    STOPWORD_PATH = 'C:\\Users\\Adriel\\Documents\\Python Scripts\\Scraping\\Config\\stopwords.txt'
    REPORT_PATH = 'C:\\Users\\Adriel\\Documents\\Python Scripts\\Scraping\\Report\\'
    REPORT_NAME = "JobReport_" + current_datetime.strftime("%Y%m%d_%H%M%S") + ".txt"
    REPORT_TITLE = "Software Developer Job Report on " + current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    KEYWORD_NAME = "JobKeyword_" + current_datetime.strftime("%Y%m%d_%H%M%S") + ".txt"
    KEYWORD_TITLE = "Software Developer Job Report (Extract) on " + current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    SEPARATOR = '=======================================================================================================================================================\n\n'
    
    config_reader = cr.Csv_Reader(CONFIG_PATH)
    
    print("Start scraping at " + str(current_datetime))
    engine = se.Scraping_Engine(config_reader.get_data())
    engine.scrape_all()
    report_writer = rw.Report_Writer(REPORT_NAME, REPORT_PATH)
    report_writer.write_title(REPORT_TITLE)
    report_writer.write_list(engine.site_list, engine.title_list, engine.company_list, engine.location_list, engine.description_list, engine.link_list, [SEPARATOR] * len(engine.site_list))
    print("Scrape completed")
    
    print("Start keyword extraction")
    extractor = ke.KeywordExtractor(STOPWORD_PATH, engine.description_list)
    extractor.extract_each_text()
    keyword_writer = rw.Report_Writer(KEYWORD_NAME, REPORT_PATH)
    keyword_writer.write_title(KEYWORD_TITLE)
    keyword_writer.write_list(engine.site_list, engine.title_list, engine.company_list, engine.location_list, extractor.keyword_list, engine.link_list, [SEPARATOR] * len(engine.site_list))
    extractor.extract_all_text()
    keyword_writer.write_text("Keywords of today's scraping: ")
    keyword_writer.write_list(extractor.keyword_list, [SEPARATOR] * len(extractor.keyword_list))
    print("Keyword extraction completed")

if __name__ == "__main__":
    main()
