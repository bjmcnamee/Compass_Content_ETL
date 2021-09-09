"""
For each drug name in 1_drugsroot.txt :
    Request drug codes (synonym, rx, drugbank, atc and spl) from NLM api for each drug name
    If drug name is a combination (includes "/") then try :
        variants of drug ("/"," / ","-"," and "," and ","+")
        reversing drug (drug1/drug2/ --> drug1/drug2)
Save drug names and codes to 1_drugscodes.txt
"""
from csv import reader
import requests
project_data = "/home/barnyard/0python/compass/Scraping_and_ETL/"

f1 = open(project_data + "/data/1_drugsroot.txt", "r")
f2 = open(project_data + "/data/1_drugscodes.txt", "w")
f3 = open(project_data + "/reports/1_drugscodes_report.txt", "w")

def getRx(drug):
    urlroot = 'http://rxnav.nlm.nih.gov/REST/rxcui.json?name='
    url = urlroot + drug
    try:
        print("Trying : ", drug)
        response = requests.get(url, timeout=5)
        dic = response.json()
        f_rx = dic["idGroup"]["rxnormId"][0]
    except KeyError:
        f_rx = "NA"
    return f_rx

def getSynonym(rx):
    urlroot = 'http://rxnav.nlm.nih.gov/REST/rxcui/'
    urlend = '/allProperties.json?prop=names+codes'
    url = urlroot + rx + urlend
    response = requests.get(url)
    dic = response.json()
    i = 0; synonym = "NA"
    if dic['propConceptGroup']['propConcept'][0]['propName'] == "RxNorm Name":
        synonym = dic['propConceptGroup']['propConcept'][0]['propValue']
    return(synonym)
    
def getDB(rx):
    urlroot = 'http://rxnav.nlm.nih.gov/REST/rxcui/'
    urlend = '/allProperties.json?prop=names+codes'
    url = urlroot + rx + urlend
    response = requests.get(url)
    dic = response.json()
    i = 0; drugbank = "NA"
    if dic == {"propConceptGroup": None}:
        drugbank = "NA"
    else:
        for i in dic['propConceptGroup']['propConcept']:
            if [i][0]['propName'] == "DRUGBANK":
                drugbank = [i][0]['propValue']
                break
            elif [i][0]['propName'] == "SPL_SET_ID":
                break
    return drugbank

def getATC(rx):
    urlroot = 'http://rxnav.nlm.nih.gov/REST/rxcui/'
    urlend = '/property.json?propName=ATC'
    url = urlroot + rx + urlend
    response = requests.get(url)
    dic = response.json()
    if dic == {"propConceptGroup":None}:
        atc = "NA"
    else:
        atc = dic["propConceptGroup"]["propConcept"][0]["propValue"] # return first ATC id which appears to match
    return atc


def mergeCodes(rx,drug,drugfound):
      drugbank = getDB(rx)                                                                                  # call function getDB() to fetch DrugBank code
      atc = getATC(rx)                                                                                      # call function getATC() to fetch ATC code
      synonym = getSynonym(rx)                                                                              # call function getSynonym() to fetch NLM drug name (sometimes different)
      codes = list([drug,drugfound,synonym,rx,drugbank,atc])                                                # add names and codes to list codes
      print(codes)                                                                                          # console output codes list
      if drug != synonym.capitalize() :                                                                     # compare drug name to synonym
          print("Found synonym")                                                                            # console output flag 'found syonym'
      codes = list(['\"',drug,'\",\"',drugfound,'\",\"',synonym,'\",\"',rx,'\",\"',drugbank,'\",\"',atc,'\"\n']) # reformat codes list with quotations and comma separators
      f2.writelines(codes)                                                                                  # write codes to f2, ie 1_drugscodes.txt
      return codes

# Main
found=[]; notfound=[]; splitfound=[]; rxlist = []; synonyms_found = []                                      # declare empty lists
lines = list(reader(f1))                                                                                    # read f1, ie 1_drugsroot.txt into list lines

for line in lines:                                                                                          # cycle through each element of lines list
    drug = line[0].lower()                                                                                  # assign value from lines to drug as lowercase
    # clean drug names - capitalise drugs
    drugfound = ''; drugs = drug.split("/")
    for k in range (0,len(drugs)):
          drugfound += drugs[k].capitalize() + "/"                                                          # capitalize drug (or drugs if two or more exist indicated by "/"
    drug = drugfound[:-1]                                                                                   # remove last "/" added above, ie drug1/drug2/ --> drug1/drug2
    drugfound = drug                                                                                        # create new var to keep final drug name
    rx = getRx(drug)
    rxlist.append(rx)                                                                                       # add to rxlist

    # process non-combination drugs
    if rx != "NA" :                                                                                         # if drug 'found'
         codes = mergeCodes(rx,drug,drugfound)                                                              # fetch other codes and add to codes list
         reportline = drug + "  -  Rx: " + codes[7] + " Drugbank: " + codes[9] + " ATC: " + codes[11]       # create report line to record 'found' drugs
         found.append(reportline)

    # process dual combination drugs variants with alternative dividers
    elif drug.count('/') == 1 :
          if rx == "NA": drugfound = drugfound.replace("/"," / "); rx = getRx(drugfound)                    # replace '/' with ' / ' then try fetch Rx id again
          if rx == "NA": drugfound = drugfound.replace(" / ","-"); rx = getRx(drugfound)                    # replace ' / ' with '-' then try fetch Rx id again
          if rx == "NA": drugfound = drugfound.replace("-"," and "); rx = getRx(drugfound)                  # replace '-' with ' and ' then try fetch Rx id again
          if rx == "NA": drugfound = drugfound.replace(" and ","+"); rx = getRx(drugfound)                  # replace ' and ' with '+' then try fetch Rx id again
          if rx == "NA": drugfound = drugfound.split("+")[1] + "/" + drugfound.split("+")[0]; rx = getRx(drugfound) # replace '+' with '/' and reverse drug terms then try fetch Rx id again
          if rx == "NA": drugfound = drugfound.replace("/"," / "); rx = getRx(drugfound)                    # replace '/' with ' / ' then try fetch Rx id again
          if rx == "NA": drugfound = drugfound.replace(" / ","-"); rx = getRx(drugfound)                    # replace ' / ' with '-' then try fetch Rx id again
          if rx == "NA": drugfound = drugfound.replace("-"," and "); rx = getRx(drugfound)                  # replace '-' with ' and ' then try fetch Rx id again
          if rx != "NA" :                                                                                   # if drug 'found'
                  codes = mergeCodes(rx,drug,drugfound)                                                     # fetch other codes and add to codes list
                  reportline = drug + " as " + drugfound + "  -  Rx: " + codes[7] + " Drugbank: " + codes[9] + " ATC: " + codes[11]
                  splitfound.append(reportline)
          else:                                                                                             # if drug not 'found' then fetch individual drug terms for combo drugs
                notfound.append(drug)                                                                       # add combination drug to notfound list
                drugs = drugfound.split(" and ")
                for i in range(0,len(drugs)):
                      print(drugs[i])
                      rx = getRx(drugs[i])
                      if rx in rxlist:                                                                      # check if rx found already - compare with rxlist
                          print(drugs[i], " already found")
                      else:
                          rxlist.append(rx)                                                                 # add to rxlist
                          codes = mergeCodes(rx,drug,drugs[i])                                              # fetch other codes and add to codes list
                          reportline = drug + " only " + drugs[i] + "  -  Rx: " + codes[7] + " Drugbank: " + codes[9] + " ATC: " + codes[11]
                          splitfound.append(reportline)

    # process 3+ combination drugs as individual drugs
    elif (rx == "NA") & (drug.count('/') >= 2):
          drugs = drugfound.split(" and ")
          for i in range(0,len(drugs)):
                print(drugs[i])
                rx = getRx(drugs[i])
                if rx in rxlist:                                                                            # check if rx found already - compare with rxlist
                    print(drugs[i]," already found")
                else:
                    rxlist.append(rx)                                                                       # add to rxlist
                    codes = mergeCodes(rx, drug, drugs[i])                                                  # fetch other codes and add to codes list
                    reportline = drug + " only " + drugs[i] + "  -  Rx: " + codes[7] + " Drugbank: " + codes[9] + " ATC: " + codes[11]
                    splitfound.append(reportline)

    else:
         notfound.append(drug)                                                                              # add to notfound list


# write report
f3.writelines("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Found XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
for i in range (0, len(found)): f3.writelines(found[i] + "\n")
f3.writelines("\nSubtotal found " + str(len(found)) + "\n")
f3.writelines("\n\nXXXXXXXXXXXXXXXX Combination Drugs Split & Found XXXXXXXXXXXXX\n")
for i in range (0, len(splitfound)): f3.writelines(splitfound[i] + "\n")
f3.writelines("\nSubtotal found " + str(len(splitfound)) + "\n\n")
f3.writelines("Total found " + str(len(found) + len(splitfound)) + "\n")
f3.writelines("\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Not Found XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
for i in range (0, len(notfound)): f3.writelines(notfound[i] + "\n")
f3.writelines("\nTotal NOT found " + str(len(notfound)) + "\n")

f1.close(); f2.close(); f3.close()

