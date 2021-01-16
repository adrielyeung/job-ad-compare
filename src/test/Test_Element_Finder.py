# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
import src.Element_Finder as ef

class Test_Element_Finder(unittest.TestCase):
    LEVEL = 'Result'
    
    def setUp(self):
        self.test_element_finder = ef.Element_Finder()
    
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_item_by_id_valid_return(self, mock_row, mock_bs):
        test_list = ['0', '1']
        item_selected = 0
        # Side effect is used to set what each call returns, each item in the list is returned in successive calls
        mock_row.__getitem__.side_effect = ['id', 'div', self.LEVEL, 'div', self.LEVEL, item_selected]
        # Return value is used when only 1 return from the function
        mock_bs.find_all.return_value = test_list
        actual_item = self.test_element_finder.find_item_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(test_list[item_selected], actual_item)
        
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_item_by_id_invalid_return(self, mock_row, mock_bs):
        test_list = []
        item_selected = 0
        mock_row.__getitem__.side_effect = ['id', 'div', self.LEVEL, 'div', self.LEVEL, item_selected]
        mock_bs.find_all.return_value = test_list
        actual_item = self.test_element_finder.find_item_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(None, actual_item)
    
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_item_by_class_valid_return(self, mock_row, mock_bs):
        test_list = ['0', '1']
        item_selected = 0
        mock_row.__getitem__.side_effect = ['class', 'class', 'div', self.LEVEL, 'div', self.LEVEL, item_selected]
        mock_bs.find_all.return_value = test_list
        actual_item = self.test_element_finder.find_item_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(test_list[item_selected], actual_item)
        
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_item_by_class_invalid_return(self, mock_row, mock_bs):
        test_list = []
        item_selected = 0
        mock_row.__getitem__.side_effect = ['class', 'class', 'div', self.LEVEL, 'div', self.LEVEL, item_selected]
        mock_bs.find_all.return_value = test_list
        actual_item = self.test_element_finder.find_item_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(None, actual_item)
    
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_item_by_none_valid_return(self, mock_row, mock_bs):
        test_list = ['0', '1']
        item_selected = 0
        mock_row.__getitem__.side_effect = ['none', 'none', 'none', 'div', 'div', item_selected]
        mock_bs.find_all.return_value = test_list
        actual_item = self.test_element_finder.find_item_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(test_list[item_selected], actual_item)
        
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_item_by_none_invalid_return(self, mock_row, mock_bs):
        test_list = []
        item_selected = 0
        mock_row.__getitem__.side_effect = ['none', 'none', 'none', 'div', 'div', item_selected]
        mock_bs.find_all.return_value = test_list
        actual_item = self.test_element_finder.find_item_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(None, actual_item)
        
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_item_by_self_valid_return(self, mock_row, mock_bs):
        mock_row.__getitem__.side_effect = ['self', 'self', 'self', 'self']
        actual_item = self.test_element_finder.find_item_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(mock_bs, actual_item)
    
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_all_by_id_valid_return(self, mock_row, mock_bs):
        test_list = ['0', '1']
        mock_row.__getitem__.side_effect = ['id', 'div', self.LEVEL]
        mock_bs.find_all.return_value = test_list
        actual_item = self.test_element_finder.find_all_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(test_list, actual_item)
        
    @patch('bs4.element.Tag')
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_all_by_class_sub_valid_return(self, mock_row, mock_bs, mock_tag):
        test_list = ['0', '1']
        mock_row.__getitem__.side_effect = ['class', 'class', 'sub', 'div', self.LEVEL, 'div']
        mock_bs.find.return_value = mock_tag
        mock_tag.find_all.return_value = test_list
        actual_item = self.test_element_finder.find_all_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(test_list, actual_item)    

    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_all_by_class_non_sub_valid_return(self, mock_row, mock_bs):
        test_list = ['0', '1']
        mock_row.__getitem__.side_effect = ['class', 'class', 'non-sub', 'div', self.LEVEL]
        mock_bs.find_all.return_value = test_list
        actual_item = self.test_element_finder.find_all_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(test_list, actual_item)
        
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_all_by_none_valid_return(self, mock_row, mock_bs):
        test_list = ['0', '1']
        mock_row.__getitem__.side_effect = ['none', 'none', 'none', 'div']
        mock_bs.find_all.return_value = test_list
        actual_item = self.test_element_finder.find_all_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(test_list, actual_item)
        
    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_all_by_self_valid_return(self, mock_row, mock_bs):
        mock_row.__getitem__.side_effect = ['self', 'self', 'self', 'self']
        actual_item = self.test_element_finder.find_all_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(mock_bs, actual_item)

    @patch('bs4.BeautifulSoup')
    @patch('pandas.Series')
    def test_find_all_by_invalid_return(self, mock_row, mock_bs):
        mock_row.__getitem__.side_effect = ['invalid', 'invalid', 'invalid', 'invalid']
        actual_item = self.test_element_finder.find_all_by(mock_row, mock_bs, self.LEVEL)
        
        self.assertEqual(None, actual_item)   

if __name__ == '__main__':
    unittest.main()
