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
        self._data = pd.read_csv(self._filepath, encoding="utf-8")
        self._data.fillna("", inplace=True)
    
    def get_data(self):
        '''
        Getter for Pandas dataframe.

        Returns
        -------
        Pandas dataframe
            Data read from CSV.
        '''
        return self._data
