"""
Scrape all drug data for each drug from Drugbank website 
Use cfscrape to avoid Drugbank using Cloudshield to block better known scraping modules
Use random time intervals to simulate human calls
Scrape all data as one blob until requirements better defined

import time, random, requests
time.sleep(random.randint(10, 3600))
r = requests.get('https://api.github.com/events')

"""

from csv import reader
import cfscrape
from bs4 import BeautifulSoup
project_data = "/home/barnyard/0python/compass/Scraping_and_ETL/"
f1 = open(project_data + "/data/2_drugscodes_all.txt", "r")                                       # input file - drugs and their codes
f2a = open(project_data + "/data/4_drugbank_content1.txt", "w")                                   # split output files to remain below SQL import file size limit
f2b = open(project_data + "/data/4_drugbank_content2.txt", "w")                                   # split output files to remain below SQL import file size limit
f3 = open(project_data + "/reports/4_drugbank_content_report.txt", "w")
f3.writelines("Drugbank page scraped\nXXXXXXXXXXXXXXXXXXXXX\n\n")
lines = list(reader(f1, quotechar='"', delimiter=','))                                      # read input file f1 and assign drug on each line to elements in list drugs

dbpages = []                                                                                # list of cleaned drugbank pages (long strings of html)
found = []; notfound = []; count = 0; charcount = 0
urlroot = "https://go.drugbank.com/drugs/"

for line in lines:
    drug = line[2]                                                                          # drug name from each line of drugs
    db_id = line[4]                                                                         # Drugbank id from each line of drugs
    url = urlroot + db_id                                                                   # create search string for each Drugbank id

    if db_id != "":
        found.append(drug)                                                                  # add to found list for reporting
        print("Scraping", drug, "...")
        scraper = cfscrape.create_scraper()                                                 # returns a CloudScraper instance
        page = scraper.get(url).content                                                     # scrape page for given url (Drugbank id)
        soup = BeautifulSoup(page, 'html.parser')                                           # create bs4 soup for given html page
        soup = soup.find('div', class_="card-content px-md-4 px-sm-2 pb-md-4 pb-sm-2")

        # clean soup by removing various html tags
        for div in soup.find_all('div', {'id': 'product-carousel-row'}):
            div.decompose()
        for div in soup.find_all('div', {'class': ['incopy-button btn btn-pink-filled','incopy-text','drugbank-icon icon-chemquery','drugbank-icon icon-zoom-in','drugbank-icon icon-expand','drugbank-icon icon-see_more','drugbank-icon icon-plus','drugbank-icon icon-information','drugbank-icon icon-table','drugbank-icon icon-list']}):
            div.decompose()
        for a in soup.find_all('a', {'class': ['btn btn-pink-filled track-link','drug-info-popup','locked-incopy locked-incopy-mobile track-link']}):
            a.decompose()
        for svg in soup.find_all('svg', {'class': 'icon'}):
            svg.decompose()
        for button in soup.find_all('button', {'class': ['btn btn-default','btn btn-outline-secondary dropdown-toggle','close']}):
            button.decompose()
        for span in soup.find_all('span', {'aria-hidden': ['true','false']}):
            span.decompose()

        for img in soup.find_all('img', {'class': ['locked-pharmacology-img', 'locked-contraindications-img', 'locked-medicalerrors-img', 'locked-interactions-img', 'locked-products-img', 'locked-drugtargets-img']}):
            img['class'] = 'img-drugbank'

        # clean soup further
        soup = str(soup).replace("\"", "\'").replace("  ", " ")                             # replace double quotes with single quotes to enable import later
        soup = soup.replace("src=\'", "src=\'https://go.drugbank.com")                      # keep link working, but link off site to drugbank

        output = '"' + drug + '","' + db_id + '","' + soup + '"\n'
        charcount += len(output)                                                            # count characters in output - single character takes exactly 8 bits, 1 byte so 1 MB = 1024 x 1024 = 1,048,576 bytes / characters
        if charcount < 1048576*30:                                                          # split output files at 30MB to remain below SQL import file size limit 50MB
            f2a.writelines(output)
        else:
            f2b.writelines(output)
        report = drug + "\n"
        f3.writelines(report)
    else:
        notfound.append(drug)                                                               # add to notfound list for reporting
        print(drug, "- Drugbank id not available")

f3.writelines("\n\nTotal : " + str(len(found)))
f3.writelines("\n\nDrugbank page NOT scraped - Drugbank id not available\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n")
for drug in notfound:
    f3.writelines(drug + "\n")
f3.writelines("\n\nTotal : " + str(len(notfound)))

f3.close(); f2a.close(); f2b.close(); f1.close()