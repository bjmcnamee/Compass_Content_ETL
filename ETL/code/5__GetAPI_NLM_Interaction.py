"""
get Drugbank interactions from NLM RxNorm db via api - easier than directly from Drugbank website
SELECT drug, rxcui, i_rxcui, COUNT(drug) FROM `drug_interactions` GROUP BY (i_rxcui)
see Notes ate end of file
"""

import requests # HTTP request returns a Response Object with all the response data (content, encoding, status, etc)
from csv import reader
project_data = "/home/barnyard/0python/compass/Scraping_and_ETL/"
f1 = open(project_data + "/data/2_drugscodes_all.txt", "r");
f2 = open(project_data + "/data/5_interactions.txt", "w");
f3 = open(project_data + "/reports/5_interactions_report.txt", "w");


def getinteractions(rx,drug):
    interactions=[]; i_count = 0; 
    global all_i_count; 
    urlroot = 'https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui='
    urlend = '&sources=DrugBank'
    url = urlroot+rx+urlend
    response = requests.get(url) # Sends a GET request to the specified url
    dic = response.json() # parse a JSON response from the requests library
    try:
       for i in dic["interactionTypeGroup"][0]["interactionType"][0]["interactionPair"]:
          i_rx = [i][0]["interactionConcept"][1]["minConceptItem"]["rxcui"]
          i_drug = [i][0]["interactionConcept"][1]["sourceConceptItem"]["name"]
          i_interaction = [i][0]["description"]
          i_all = '\"'+drug+'\",\"'+rx+'\",\"'+i_drug+'\",\"'+i_rx+'\",\"'+i_interaction+'\"'
          interactions.append(i_all)
          i_count += 1
          if i_interaction.find('\"')!=-1: print(i_interaction)
       all_i_count += i_count
       reportline = drug + " : " + str(i_count) + " interactions\n"
       print(reportline, end="")
       f3.writelines(reportline)
    except KeyError:
       reportline = drug + " - KEY ERROR : 0 interactions\n"
       print(reportline)
       interactions = ""
       pass
    return interactions

lines = list(reader(f1, delimiter=','))
allinteractions=[];rx_list=[];all_i_count = 0; nonefound=[]; found=[]

f3.writelines("FOUND DRUG-DRUG INTERACTIONS\n")
f3.writelines("----------------------------\n")

for line in lines: # cycle through list rows
    rx = line[3] # fetch rx code
    drug = line[2] # for troubleshooting via console print and report
    interactions = getinteractions(rx,drug) # fetch all rx interactions and add to list
    if interactions != "":
        allinteractions.append(interactions)
        found.append(drug)
    else:
        nonefound.append(drug)

reportline = "Total drugs : "+str(len(found))+"\n"
f3.writelines(reportline)
f3.writelines("\nNOT FOUND DRUG-DRUG INTERACTIONS - either NLM records no interactions or error processing API JSON file for this drug\n")
f3.writelines("-----------------------------------------------------------------------------------------------------------------------\n")

for i in range(0,len(nonefound)):
      reportline = (nonefound[i])+"\n" 
      f3.writelines(reportline)
reportline = "Total drugs : "+str(len(nonefound))+"\n"
f3.writelines(reportline)

for _list in allinteractions:
  for _string in _list:
      output = str(_string) + '\n'  
      f2.writelines(output)
          
f3.close(); f2.close(); f1.close()

"""
Importing large files - change default 5mins to 'no time limit'
Open configuration file \phpmyadmin\libraries\config.default.php
change $cfg['ExecTimeLimit'] = 300; to $cfg['ExecTimeLimit'] = 0;

Examples of some drugs with no interactions found in NLM and, for some drugs, Drugbank has interactions : 
Carbomer 235535 
Gold 1311190
Lithium 6448
Olopatadine 135391
Polyvinyl alcohol 8570
Sodium cromoglycate 3538
Sodium hyaluronate 42892
Sodium alginate 56446
Somatropin 61148
"""
