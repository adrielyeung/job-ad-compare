# -*- coding: utf-8 -*-
import src.Scraping_Engine as se
import src.Csv_Reader as cr
import src.Report_Writer as rw
import src.Excel_Writer as ew
import src.Keyword_Extractor as ke
from src.__init__ import get_root_path
import logging
import traceback

def main(config_path, stopword_path, report_path, category, location, msgLabel, current_datetime):
    REPORT_NAME = category.replace(' ', '') + "JobReport_" + location.replace(' ', '') + "_" + current_datetime.strftime("%Y%m%d_%H%M%S") + ".txt"
    REPORT_TITLE = category + " Job Report in " + location + " on " + current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    KEYWORD_NAME = category.replace(' ', '') + "JobKeyword_" + location.replace(' ', '') + "_" + current_datetime.strftime("%Y%m%d_%H%M%S") + ".txt"
    KEYWORD_TITLE = category + " Job Keyword in " + location + " on " + current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    SEPARATOR = '=======================================================================================================================================================\n\n'
    msg = ""
    
    try:
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
        extractor = ke.KeywordExtractor(stopword_path, engine.description_list, engine.title_list, engine.company_list, engine.location_list, category + ' ' + location)
        extractor.extract_each_text()
        keyword_writer = rw.Report_Writer(KEYWORD_NAME, report_path)
        keyword_writer.write_title(KEYWORD_TITLE)
        keyword_writer.write_list(engine.site_list, engine.title_list, engine.company_list, engine.location_list, extractor.keyword_list, engine.link_list, [SEPARATOR] * len(engine.site_list))
        extractor.extract_all_text()
        keyword_writer.write_text("Keywords of today's scraping: ")
        keyword_writer.write_list(extractor.keyword_list, [SEPARATOR] * len(extractor.keyword_list))
        msg += "Keyword extraction completed"
        msgLabel.setText(msg)
    except Exception:
        log(get_root_path() + 'Log\\', traceback.format_exc(), current_datetime)
        raise

def main_excel(config_path, stopword_path, report_path, category, location, msgLabel, current_datetime):
    REPORT_NAME = category.replace(' ', '') + "JobReport_" + location.replace(' ', '') + "_" + current_datetime.strftime("%Y%m%d_%H%M%S") + ".xlsx"
    msg = ""
    
    try:
        config_reader = cr.Csv_Reader(config_path)
        msg += "Start scraping at " + str(current_datetime) + "\nReport path at " + report_path + REPORT_NAME + "\n"
        msgLabel.setText(msg)
        engine = se.Scraping_Engine(config_reader.get_data(), category, location, excel=True)
        engine.scrape_all()
        
        msg += "Scrape completed\nStart Excel report generation\n"
        msgLabel.setText(msg)
        excel_writer = ew.Excel_Writer(REPORT_NAME, report_path)
        excel_writer.write(engine.site_list, engine.company_list, engine.title_list, engine.description_list, engine.skills_list, engine.location_list, engine.link_list)
        msg += "Excel report generation completed"
        msgLabel.setText(msg)
    except Exception:
        log(get_root_path() + 'Log\\', traceback.format_exc(), current_datetime)
        raise

def log(log_path, msg, current_datetime):
    logging.basicConfig(filename=log_path + current_datetime.strftime("%Y%m%d_%H%M%S") + ".log", level=logging.DEBUG)
    logging.error(msg)
