# -*- coding: utf-8 -*-
import pandas as pd

class Excel_Writer:
    '''
    Writes into an Excel report.
    '''
    def __init__(self, filename, filepath):
        '''
        Initialises the report writer.

        Parameters
        ----------
        filename : string
            File name.
        filepath : string
            Directory path (without filename).
        '''
        self._filename = filename
        self._filepath = filepath
        
    def write(self, *lists):
        '''
        Compiles report from a list of titles, contents, etc.

        Parameters
        ----------
        *lists : any number of lists
            Lists to compile report from. Each list should contain 1 element of the report.
            Lists should be ordered in the way they are shown in the report.
            E.g. [title1, title2, ...], [content1, content2, ...], [ending1, ending2, ...]
            for a report with title, followed by content, finally ending.
        '''
        zipped = list(zip(*lists))
        self._file = pd.DataFrame(data=zipped, columns=["Site", "Company", "Job title", "Description", "Skills", "Location", "Link"])
        
        self._file.to_excel(self._filepath + self._filename)
