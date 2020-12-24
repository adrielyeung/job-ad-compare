# -*- coding: utf-8 -*-

class Element_Finder:
        
    def find_item_by(self, row, upper_level_object, extraction_level):
        '''
        Find matching HTML element with specified attributes from config file (if 
        >1 matching elements, return the one as specified by 
        <extraction_level>_item in the config file).
    
        Parameters
        ----------
        row : pandas.Series
            Contains a row of data from config file.
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
    
    def find_all_by(self, row, upper_level_object, extraction_level):
        '''
        Find all matching HTML element with specified attributes from config file.
    
        Parameters
        ----------
        row : pandas.Series
            Contains a row of data from config file.
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
        if row['{}_attribute'.format(extraction_level)] == "id":
            return upper_level_object.find_all(row['{}_name'.format(extraction_level)], id=row['{}_tag'.format(extraction_level)])
        elif row['{}_attribute'.format(extraction_level)] == "class":
            if row['{}_item'.format(extraction_level)] == 'sub':
                return upper_level_object.find(row['{}_name'.format(extraction_level)], class_=row['{}_tag'.format(extraction_level)]).find_all(row['{}_name'.format(extraction_level)], recursive=False)
            else:
                return upper_level_object.find_all(row['{}_name'.format(extraction_level)], class_=row['{}_tag'.format(extraction_level)])
        elif row['{}_attribute'.format(extraction_level)] == "none":
            return upper_level_object.find_all(row['{}_name'.format(extraction_level)])
        elif row['{}_attribute'.format(extraction_level)] == "self":
            return upper_level_object
        return None
