# job-ad-compare
Compare job ads from several sites, to obtain an optimal job opportunity.

This project aims to use web scraping technology of Python, namely BeautifulSoup and Selenium, to extract job postings of a certain role (e.g. software developer) from various sites. The descriptions are then fed to a Scikit-Learn model to extract the most important keywords related to that role, so as to determine the most important skills required.

Project is still in development, current status is that the descriptions could be extracted from various sites.

To generalise the extraction algorithm, the HTML tags containing the relevant information are stored as config in the ```job_ad_sites.csv``` file. A sample of those tags are uploaded. To find the config, the job posting website HTML page needs to be analysed with Chrome web developer tool first.
