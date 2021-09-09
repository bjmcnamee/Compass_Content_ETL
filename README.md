# Compass Database
- Expert system for GPs/Pharmacists
- Drug-drug interactions, Drug-disease interactions, Drug-gene interactions and more
- <a href="https://github.com/bjmcnamee/Compass_Application">Application</a> built in MySQL/PHP/Javascript/CSS
- Content API/Scraping collection and cleaning via Python ETL tools
- 561K+ drug-drug interactions, 766 drugs
####
####
#### 0__CleanDrugs.py - clean drug names

#### 1__GetAPI_NLM_Codes.py - API fetch various catalogue codes via API from National Library of Medicine <a href="https://mor.nlm.nih.gov/RxNav/">RxNav app</a>
- codes include : ATC, DRUGBANK, RxCUI, SPL_SET_ID
- requests lib

#### 2__GetSPLs_FuzzyMatch.py
- API fetch all SPL_SET_ID for each drug and find best match using fuzzy match
- lib Levenshtein

#### 3__ScrapeDailyMeds.py
- scrape and parse drug profile from <a href="https://dailymed.nlm.nih.gov/dailymed/">DailyMed website</a> for each drug
- lib urllib.request and BeautifulSoup

#### 4__ScrapeDrugbank.py
- scrape and parse drug profile from <a href="https://go.drugbank.com/drugs">Drugbank website</a> for each drug
- lib cfscrape and BeautifulSoup

#### 5__GetAPI_NLM_Interaction.py
 - API fetch (requests lib) various catalogue codes via API from National Library of Medicine <a href="https://mor.nlm.nih.gov/RxNav/">RxNav app</a>
