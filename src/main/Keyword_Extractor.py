# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import re

class KeywordExtractor:
    '''
    Extracts keywords from a text using Tf-Idf method, based on a list of other texts.
    '''
    MAX_DF = 0.85
    NUM_KEYWORDS = 10
    
    def __init__(self, stopword_path, description_list):
        '''
        Initialises the keyword extractor.

        Parameters
        ----------
        stopword_path : string
            File path of stopword list to use.
        description_list : list
            List of job descriptions (texts to extract keywords from).

        Returns
        -------
        None.
        '''
        self._stopwords = self._get_stop_words(stopword_path)
        self._count_vectorizer = CountVectorizer(max_df= self.MAX_DF, stop_words = self._stopwords)
        self._description_list = description_list
        self._word_count_vector = self._count_vectorizer.fit_transform(self._description_list)
        self._tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        self._tfidf_transformer.fit(self._word_count_vector)
        
    def extract(self, textlist):
        '''
        Extracts keywords in a list of text, keywords are stored into new list, self.keyword_list.
        
        Parameters
        ----------
        textlist : list of string
            Input text.

        Returns
        -------
        None.
        '''
        self.keyword_list = []
        for i in range(len(textlist)):
            tf_idf_vector = self._tfidf_transformer.transform(self._count_vectorizer.transform([textlist[i]]))
            sorted_items = self._sort_coo(tf_idf_vector.tocoo())
            keywords = self._extract_top_n_from_vector(self._count_vectorizer.get_feature_names(), sorted_items, self.NUM_KEYWORDS)
            keyword_string = ""
            for k in keywords:
                keyword_string += k.title() + " "
            self.keyword_list.append(keyword_string + '\n')
    
    def extract_each_text(self):
        '''
        Extracts keywords from each text in description_list, using Tf-Idf score by comparing with other texts in the list.

        Returns
        -------
        None.
        '''
        self.extract(self._description_list)
    
    def extract_all_text(self):
        '''
        Extracts keywords from all text in description_list.
        (Note: not sure if this can work since there is not a library of "other text")

        Returns
        -------
        None.
        '''
        description_all = ""
        for description in self._description_list:
            description_all += description
        self.extract([description_all])
            
    def _get_stop_words(self, stopwords_file_path):
        '''
        Returns a set of stopwords based on config file, path as specified by
        stopwords_file_path.
    
        Parameters
        ----------
        stopwords_file_path : string
            File path of stop word list.
    
        Returns
        -------
        frozenset(stop_set) : frozenset
            Stop word set (cannot be modified).
    
        '''
        # load stop words
        with open(stopwords_file_path, 'r', encoding="utf-8") as f:
            stopwords = f.readlines()
            stop_set = set(m.strip() for m in stopwords)
            return frozenset(stop_set) 
    
    def _pre_process(self, text):
        '''
        Returns pre-processed text, converting into lowercase letters and remove symbols 
        and numbers (except characters +, #, ' and . which are useful in current 
                     keyword extraction).
    
        Parameters
        ----------
        text : string
            Text to process.
    
        Returns
        -------
        text : string
            Text returned.
    
        '''
        # Convert to lowercase
        text = text.lower()
        # Remove special characters that are of no use
        # Mind the apostrophe ’ is not the same as the quote '
        text = re.sub('(\\d|[^+#.’\\w\'])+',' ', text)
        # Remove full stop (recognised by space after it or end of string)
        text = re.sub('\\.\s', ' ', text)
        text = re.sub('\\.$', '', text)
        text = re.sub('’','\'', text)
        return text
    
    def _sort_coo(self, coo_vector):
        '''
        Sorts the coordinate vector in descending order of values.
        
        Parameters
        ----------
        coo_vector : scipy.sparse.csr_matrix
            Vector to sort.
            
        Returns
        -------
        tuple, sorted by values (data) in descending order.
        '''
        tuples = zip(coo_vector.col, coo_vector.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def _extract_top_n_from_vector(self, feature_names, sorted_items, n=10):
        '''
        Get the feature names and TfIdf score of top n items (with max TfIdf score).
        
        Parameters
        ----------
        feature_names : list
            Feature names of CountVectorizer.
        sorted_items : tuple
            Sorted COO matrix in descending order.
        n : int, default 10
            Number of items to extract.
        '''
        # Extract top n items from vector
        sorted_items = sorted_items[:n]
        
        score_vals = []
        feature_vals = []
        
        # Word index and corresponding TfIdf score
        for idx, score in sorted_items:
            # Keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])
            
        # Create a dictionary of (feature, score)
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]
        
        return results
