# -*- coding: utf-8 -*-
import unittest
import os
import Report_Writer as rw

class Test_Report_Writer(unittest.TestCase):
    
    TEST_FILENAME = 'Report_test.txt'
    TEST_PATH = 'C:\\Users\\Adriel\\Documents\\Python Scripts\\Scraping\\Report\\'
    TEST_TITLE = 'Test title'
    TEST_STRING1 = '1'
    TEST_STRING2 = '2'
    TEST_STRING3 = '3'
    TEST_STRING4 = '4'
    
    def setUp(self):
         self.test_report_writer = rw.Report_Writer(self.TEST_FILENAME, self.TEST_PATH)
         
    def test_write_title(self):
        self.test_report_writer.write_title(self.TEST_TITLE)
        expected_input = self.TEST_TITLE + '\n====================================================\n'
        
        with open(self.TEST_PATH + self.TEST_FILENAME, 'r', encoding='utf-8') as f:
            self.assertEqual(expected_input, f.read())
    
    def test_write_list(self):
        test_list_1 = [self.TEST_STRING1, self.TEST_STRING3]
        test_list_2 = [self.TEST_STRING2, self.TEST_STRING4]
        
        self.test_report_writer.write_list(test_list_1, test_list_2)
        
        expected_input = 'Number: 1\n' + self.TEST_STRING1 + self.TEST_STRING2 + 'Number: 2\n' + self.TEST_STRING3 + self.TEST_STRING4
        
        with open(self.TEST_PATH + self.TEST_FILENAME, 'r', encoding='utf-8') as f:
            self.assertEqual(expected_input, f.read())
    
    def test_write_text(self):
        self.test_report_writer.write_text(self.TEST_TITLE)
        expected_input = self.TEST_TITLE + '\n'
        
        with open(self.TEST_PATH + self.TEST_FILENAME, 'r', encoding='utf-8') as f:
            self.assertEqual(expected_input, f.read())
    
    def tearDown(self):
        os.remove(self.TEST_PATH + self.TEST_FILENAME)
        
if __name__ == '__main__':
    unittest.main()
