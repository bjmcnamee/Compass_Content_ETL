"""
Scrape interaction only drug data for each drug from Daily Med website using SPL id
"""
import urllib.request
from csv import reader
from bs4 import BeautifulSoup
project_data = "/home/barnyard/0python/compass/Scraping_and_ETL/"
f1 = open(project_data + "/data/2_drugscodes_all.txt", "r");                          # Drugs codes for each drug
f2 = open(project_data + "/data/3_dmcontent.txt", "w");                               # Daily Med content for each SPL found
f3 = open(project_data + "/reports/3_dmcontentreport.txt", "w");                # output as a report

lines = list(reader(f1,delimiter=","))                                           # read codes into lines list
found = []; notfound = []; missingspl = []                                      # separate lists by lookup status for report
urlroot = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid="

# cycle through SPL SET codes
for line in lines:
    spl = line[7]
    drug = line[2]
    url = urlroot + spl
    line.append("NA")
    report = line[2] + "\n"
    if spl == "" :
       i_section = "Missing SPL id"
       missingspl.append(report)
    else:
       page = urllib.request.urlopen(url)
       soup = BeautifulSoup(page, 'html.parser')
       i_section = "none found"
       # out of range for some drugs as tag appears with different ids
       try:
             for j in range (7,12):
                 i_id = 'anch_dj_dj-dj_'+str(j)
                 i_title = soup.find('a', id=i_id)
                 if "DRUG INTERACTIONS" in i_title.text:
                    i_section = str(i_title.find_next_siblings('div', class_='Section toggle-content closed long-content'))[1:-1]
             i_list = ["\"",drug,"\",\"",spl,"\",\"",i_section.replace("\"",",\'"),"\"\n"] # output content
             f2.writelines(i_list) # write output
             print("Scraping", drug, "...") # progress display
             found.append(report)
       except AttributeError:
             notfound.append(report)
             print("AttributeError : " + drug) # progress display
             continue
            
f3.writelines("FOUND DAILYMED INTERACTIONS\n")
f3.writelines("---------------------------\n")
for i in range(0,len(found)) :
      f3.writelines(found[i])
total = "TOTAL FOUND : " + str(i+1) + "\n"
f3.writelines(total)

f3.writelines("\n\nATTRIBUTE ERROR (SCRAPING ISSUE)\n")
f3.writelines("---------------------------\n")
for i in range(0,len(notfound)) :
      f3.writelines(notfound[i])
total = "TOTAL FOUND : " + str(i+1) + "\n"
f3.writelines(total)

f3.writelines("\n\nMISSING SPL ID\n")
f3.writelines("---------------------------\n")
for i in range(0,len(missingspl)) :
      f3.writelines(missingspl[i])
total = "TOTAL FOUND : " + str(i+1) + "\n"
f3.writelines(total)
            
f1.close(); f2.close(); f3.close()