# Expert System Content Development
- Expert system for GPs/Pharmacists
- Drug-drug interactions, Drug-disease interactions, Drug-gene interactions and more
- <a href="https://github.com/bjmcnamee/Compass_Application">Application</a> built in MySQL/PHP/Javascript/CSS
- Content API/Scraping collection and cleaning via Python ETL tools
- 561K+ drug-drug interactions, 766 drugs
####
####
#### <a href="https://github.com/bjmcnamee/Compass_ETL/blob/main/ETL/code/0__CleanDrugs.py">0__CleanDrugs.py</a>
- clean drug names

#### <a href="https://github.com/bjmcnamee/Compass_ETL/blob/main/ETL/code/1__GetAPI_NLM_Codes.py">1__GetAPI_NLM_Codes.py</a>
- fetch catalogue codes for each drug : ATC, DRUGBANK, RxCUI, SPL_SET_ID
- from National Library of Medicine (NLM) <a href="https://mor.nlm.nih.gov/RxNav/">RxNav app</a> API
- lib : requests

#### <a href="https://github.com/bjmcnamee/Compass_ETL/blob/main/ETL/code/2__GetSPLs_FuzzyMatch.py">2__GetSPLs_FuzzyMatch.py</a>
- fetch all SPL_SET_ID for each drug from NLM API
- scrape/parse drug title for each SPL_SET_ID from <a href="https://dailymed.nlm.nih.gov/dailymed/">DailyMed website</a> 
- find best match using fuzzy match
- lib : requests, Levenshtein, BeautifulSoup

#### <a href="https://github.com/bjmcnamee/Compass_ETL/blob/main/ETL/code/3__ScrapeDailyMeds.py">3__ScrapeDailyMeds.py</a>
- scrape/parse drug profile from <a href="https://dailymed.nlm.nih.gov/dailymed/">DailyMed website</a> for each drug
- lib : urllib.request, BeautifulSoup

#### <a href="https://github.com/bjmcnamee/Compass_ETL/blob/main/ETL/code/4__ScrapeDrugbank.py">4__ScrapeDrugbank.py</a>
- scrape/parse drug profile from <a href="https://go.drugbank.com/drugs">Drugbank website</a> for each drug
- lib : cfscrape and BeautifulSoup

#### <a href="https://github.com/bjmcnamee/Compass_ETL/blob/main/ETL/code/5__GetAPI_NLM_Interaction.py">5__GetAPI_NLM_Interaction.py</a>
- fetch all drug-drug interactions for each drug 
- from National Library of Medicine <a href="https://mor.nlm.nih.gov/RxNav/">RxNav app</a> API
- lib : requests
