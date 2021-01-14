# -*- coding: utf-8 -*-
class Report_Writer:
    '''
    Writes info into a .txt report.
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

        Returns
        -------
        None.
        '''
        self._filename = filename
        self._filepath = filepath
    
    def write_title(self, title):
        '''
        Creates a new file at filepath and writes title into the file.
        If exists file at filepath, replaces the file.

        Parameters
        ----------
        title : string
            DESCRIPTION.

        Returns
        -------
        None.
        '''
        with open(self._filepath + self._filename, 'w', encoding='utf-8') as f:
            f.write(title + '\n')
            f.write("====================================================\n")
    
    def write_list(self, *lists):
        '''
        Compiles report from a list of titles, contents, etc.

        Parameters
        ----------
        *lists : any number of lists
            Lists to compile report from. Each list should contain 1 element of the report.
            Lists should be ordered in the way they are shown in the report.
            E.g. [title1, title2, ...], [content1, content2, ...], [ending1, ending2, ...]
            for a report with title, followed by content, finally ending.

        Returns
        -------
        None.
        '''
        zipped = list(zip(*lists))
        with open(self._filepath + self._filename, 'a', encoding='utf-8') as f:
            for i in range(len(zipped)):
                f.write("Number: " + str(i+1) + "\n")
                f.write(''.join(zipped[i]))
    
    def write_text(self, text):
        '''
        Writes a line of text with newline at the end.

        Parameters
        ----------
        text : string
            Text to write.

        Returns
        -------
        None.
        '''
        with open(self._filepath + self._filename, 'a', encoding='utf-8') as f:
            f.write(text + '\n')
