"""
4__ScrapeDrugbank.py only returns 1 in 4 spl ids when scraping for Drugbank drug interactions so we need to use fuzzy match to find best match

For each drug name in 1_drugsroot.txt :
    Request all SPLset ids and titles from NLM api for each Rx
    Find best fuzzy match title and SPLset id for each drug name
Save drug name, rx, spl (multiple), spl title (multiple)      

3__ScrapeDailyMeds.py uses SPLset id in 1_drugscodes.txt to find interactions - needs to be changed TBD

NB Takes approx 2 days to run
"""

from csv import reader
from bs4 import BeautifulSoup
import urllib.request
import requests
import Levenshtein as fuzzy

project_data = "/home/barnyard/0python/compass/Scraping_and_ETL/"
f1 = open(project_data + "/data/1_drugscodes.txt", "r")
f2 = open(project_data + "/data/2_allSPLs.txt", "w")

def getSPLs(rx):
    # search for all SPL codes matching Rx on NLM RxNav via API
    SPL_list=[]
    urlroot = 'https://rxnav.nlm.nih.gov/REST/rxcui/'
    urlend = '/property.json?propName=SPL_SET_ID'
    url = urlroot + rx + urlend
    response = requests.get(url)
    dic = response.json()
    if dic == {"propConceptGroup":None}:
        SPL = "NA"
        SPL_list.append(SPL) # add to list of spl set ids
    else:
        for i in dic['propConceptGroup']['propConcept']:
              SPL = [i][0]["propValue"] # return first SPL id which appears to match
              SPL_list.append(SPL) # add to list of SPL ids
    return SPL_list

def getSPLtitle(drug,rx,SPL_list):
    # search for all SPL titles matching SPL on Daily Med via scrape module
    urlroot = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid="
    title = ""; SPLmatch = ""; distance = 100; flag = "on"
    print(drug)
    for i in range(len(SPL_list)) :                                                 # cycle through list of SPL ids
        url = urlroot + SPL_list[i]
        page = urllib.request.urlopen(url)                                          # fetch page
        soup = BeautifulSoup(page, 'html.parser')                                   # convert page to soup object
        soup_title = soup.find(class_='long-title', id='drug-label')                # find page title in soup object
        try:
            title = soup_title.get_text()                                           # return text string from page title
        except AttributeError: title = "NA"                                         # return 'NA' string if previous fails
        title_temp = title                                                          # create temp title var
        form_strings = [" tablet"," capsule"," solution"," powder"," gel"," injection"," cream"," solution"," suspension"," drops"] # form of drug for removal
        for form_string in form_strings:                                            # cycle through form strings
            title_temp = title_temp.replace(form_string, "")                        # remove any form strings from temp title
        distance_temp = fuzzy.distance(drug.lower(),title_temp.lower())             # measure fuzzy distance between drug name and temp title
        if distance_temp < distance :                                               # if fuzzy distance < previous distance
            SPLmatch = '\"' + drug + '\",\"' + rx + '\",\"' + SPL_list[i] + '\",\"' + title + '\"\n'  # create function return string with selected spl title and id
            distance = distance_temp                                                # update distance var with new fuzzy distance
            if flag == "on" :                                                       # flag to determine first match
                print("MATCH", distance, ":", title, SPL_list[i])                   # console test output
                flag = "off"                                                        # switch flag off
            else :
                print("BETTER MATCH", distance, ":", title, SPL_list[i])            # console test output - for matches 2,3...

        else :
            print("Ignoring :", title)                                              # console test output
        if distance_temp == 0 or i == len(SPL_list)-1 :                                # if exact match (without form strings)
            print("BEST MATCH :", SPLmatch)                              # console test output
            break                                                                   # break loop and return to main program
    return SPLmatch

lines = list(reader(f1, quotechar='"', delimiter=',')) # read input file f1 and assign drug on each line to elements in list drugs
SPL_Title_list = []; codes_output = []

for line in lines:                                             # cycle through list drugs
    drug = line[1]                                             # get drug name from drugs list
    rx = line[2]                                               # get Rx code from drugs list
    if rx != "NA" :                                         # process non-combination drugs
        SPL_list = getSPLs(rx)                              # search for all SPL codes matching Rx on NLM RxNav via API
        SPLmatch = getSPLtitle(drug,rx,SPL_list)            # search for all SPL titles matching SPL on Daily Med via scrape module
        f2.writelines(SPLmatch)                             # write to f2 file

f1.close(); f2.close()

# Addendum - merge spl code in 2_allSPLs.txt with codes in 1_drugscodes.txt in new code file 2_drugscodes_all.txt
import pandas as pd
import csv
project_data = "/home/barnyard/0python/compass/Scraping_and_ETL/"
a=pd.read_csv(project_data + "/data/1_drugscodes.txt", header=None)
b=pd.read_csv(project_data + "/data/2_allSPLs.txt", header=None)
merged = a.merge(b, on=0) # merge on drug name in column 0
merged.to_csv(project_data + "/data/2_drugscodes_all.txt", index=False, quoting=csv.QUOTE_ALL, header=None)
