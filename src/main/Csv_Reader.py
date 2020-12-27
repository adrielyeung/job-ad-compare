# -*- coding: utf-8 -*-
import pandas as pd

class Csv_Reader:
    '''
    Reads a CSV file, and set default value -999999 for NaN values.
    '''
    def __init__(self, filepath):
        '''
        Initialises the reader.

        Parameters
        ----------
        filepath : string
            Filepath to read from.

        Returns
        -------
        None.
        '''
        self._filepath = filepath
        self._data = pd.read_csv(self._filepath)
        self._data.fillna(-999999, inplace=True)
        self._data.Result_item = self._data.Result_item.astype(int)
        self._data.Title_item = self._data.Title_item.astype(int)
        self._data.Company_item = self._data.Company_item.astype(int)
        self._data.Location_item = self._data.Location_item.astype(int)
        self._data.Description_item = self._data.Description_item.astype(int)
        self._data.URL_item = self._data.URL_item.astype(int)
    
    def get_data(self):
        '''
        Getter for Pandas dataframe.

        Returns
        -------
        Pandas dataframe
            Data read from CSV.
        '''
        return self._data
    