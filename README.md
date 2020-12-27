# job-ad-compare
Compare job ads from several sites, to obtain an optimal job opportunity.

This project aims to use web scraping technology of Python, namely BeautifulSoup and Selenium, to extract job postings of a certain role (e.g. software developer) from various sites. The descriptions are then fed to a Scikit-Learn model to calculate TF-IDF scores for each vocabulary, to extract the most important keywords related to that role, so as to determine the most important skills required.

Project is still in development, current status is that the descriptions could be extracted from various sites, and keywords can be extracted from them.

From testing results, it seems that some irrevelant words often show up as keywords, thus the stopword list needs to be modified.

How to use
----------
To generalise the extraction algorithm, the HTML tags containing the relevant information are stored as config in the ```job_ad_sites.csv``` file. A sample of those tags are uploaded. To obtain the config (i.e. HTML tags needed), the job posting website HTML page needs to be analysed with Chrome web developer tool first.

The scripts ```Scraping_Controller.py``` in the ```Scraping_Scripts``` folder could be directly run. For my testing and thought process, please refer to the Jupyter notebooks in ```Scraping_Test``` folder.

Future developments
-------------------
1. Generalise the program to be able to take in any query keywords (i.e. variable in the ```?q={}``` in the URL) for job role and location.
2. Scraping of multiple pages of results.
3. Addition of certain fake keywords to the stopword list (need further testing to identify).
4. Removal of company name for keyword result, replaced by the next word.
5. Addition of a UI for inputting new scraping sites and HTML tags, also to trigger whole scraping process.
6. Consideration of using other texts as a control sample to calculate the IDF score.

Credits
-------
Credits to the fantastic tutorial in [BeautifulSoup](https://realpython.com/beautiful-soup-web-scraper-python/), [Selenium](https://www.scrapingbee.com/blog/selenium-python/) and [TF-IDF calculations](https://kavita-ganesan.com/extracting-keywords-from-text-tfidf/#.X9TbfdgzaM9)
