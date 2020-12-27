# -*- coding: utf-8 -*-
import unittest
import Keyword_Extractor as ke
from scipy.sparse import coo_matrix
import numpy as np
import os

class Test_Keyword_Extractor(unittest.TestCase):
    
    def setUp(self):
        self.TEST_FILENAME = 'C:\\Users\\Adriel\\Documents\\Python Scripts\\Scraping\\Config\\stopwords_test.txt'
        with open(self.TEST_FILENAME, 'w', encoding='utf-8') as f:
           f.write('hello\nworld')
           
        self.expected_stop_word_set = frozenset({'hello', 'world'})
        self.test_list = ['hello world', 'this is a testing class', 'this', 'ends']
        row  = np.array([0, 3, 1, 0])
        col  = np.array([0, 3, 1, 2])
        data = np.array([4, 5, 7, 9])
        self.test_matrix = coo_matrix((data, (row, col)), shape=(4, 4))
        
        self.test_extractor = ke.KeywordExtractor(self.TEST_FILENAME, self.test_list)
        self.actual_tuple = self.test_extractor._sort_coo(self.test_matrix)
        
    def test_extract(self):
        self.test_extractor.extract(self.test_list)
        self.assertNotEqual([], self.test_extractor.keyword_list)
        
    def test__get_stop_words(self):
        actual_stop_word_set = self.test_extractor._get_stop_words(self.TEST_FILENAME)
        self.assertEqual(self.expected_stop_word_set, actual_stop_word_set)
    
    def test__pre_process_convert_lower(self):
        test_string = 'ABC DEF GHI'
        expected_string = test_string.lower()
        actual_string = self.test_extractor._pre_process(test_string)
        self.assertEqual(expected_string, actual_string)
    
    def test__pre_process_remove_unimportant_chars(self):
        test_string = 'ABC.DEF. GHI\'+#.’$%@!,^&*()<>/?0123456789.'
        expected_string = 'abc.def ghi\'+#.\' '
        actual_string = self.test_extractor._pre_process(test_string)
        self.assertEqual(expected_string, actual_string)
        
    def test__sort_coo(self):
        expected_tuple = sorted(zip(self.test_matrix.col, self.test_matrix.data), key=lambda x: (x[1], x[0]), reverse=True)
        self.actual_tuple = self.test_extractor._sort_coo(self.test_matrix)
        self.assertEqual(expected_tuple, self.actual_tuple)
    
    def test__extract_top_n_from_vector(self):
        n = 10
        
        sorted_items = self.actual_tuple[:n]
        
        score_vals = []
        feature_vals = []
        
        # Word index and corresponding TfIdf score
        for idx, score in sorted_items:
            # Keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(self.test_list[idx])
            
        # Create a dictionary of (feature, score)
        expected_results = {}
        for idx in range(len(feature_vals)):
            expected_results[feature_vals[idx]] = score_vals[idx]
        
        actual_results = self.test_extractor._extract_top_n_from_vector(self.test_list, self.actual_tuple, n)
        self.assertEqual(expected_results, actual_results)
        
    def tearDown(self):
        os.remove(self.TEST_FILENAME)
        
if __name__ == '__main__':
    unittest.main()
