# -*- coding: utf-8 -*-
import src.Scraping_Engine as se
import src.Csv_Reader as cr
import src.Report_Writer as rw
import src.Keyword_Extractor as ke
from datetime import datetime
    
def main(config_path, stopword_path, report_path, category, location, msgLabel):
    current_datetime = datetime.now()
    REPORT_NAME = "JobReport_" + current_datetime.strftime("%Y%m%d_%H%M%S") + ".txt"
    REPORT_TITLE = "Software Developer Job Report on " + current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    KEYWORD_NAME = "JobKeyword_" + current_datetime.strftime("%Y%m%d_%H%M%S") + ".txt"
    KEYWORD_TITLE = "Software Developer Job Report (Extract) on " + current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    SEPARATOR = '=======================================================================================================================================================\n\n'
    msg = ""
    
    config_reader = cr.Csv_Reader(config_path)
    
    msg += "Start scraping at " + str(current_datetime) + "\nReport path at " + report_path + REPORT_NAME + "\n"
    msgLabel.setText(msg)
    engine = se.Scraping_Engine(config_reader.get_data(), category, location)
    engine.scrape_all()
    report_writer = rw.Report_Writer(REPORT_NAME, report_path)
    report_writer.write_title(REPORT_TITLE)
    report_writer.write_list(engine.site_list, engine.title_list, engine.company_list, engine.location_list, engine.description_list, engine.link_list, [SEPARATOR] * len(engine.site_list))
    msg += "Scrape completed\nStart keyword extraction\n"
    
    msgLabel.setText(msg)
    extractor = ke.KeywordExtractor(stopword_path, engine.description_list, engine.company_list, engine.location_list)
    extractor.extract_each_text()
    keyword_writer = rw.Report_Writer(KEYWORD_NAME, report_path)
    keyword_writer.write_title(KEYWORD_TITLE)
    keyword_writer.write_list(engine.site_list, engine.title_list, engine.company_list, engine.location_list, extractor.keyword_list, engine.link_list, [SEPARATOR] * len(engine.site_list))
    extractor.extract_all_text()
    keyword_writer.write_text("Keywords of today's scraping: ")
    keyword_writer.write_list(extractor.keyword_list, [SEPARATOR] * len(extractor.keyword_list))
    msg += "Keyword extraction completed"
    msgLabel.setText(msg)
