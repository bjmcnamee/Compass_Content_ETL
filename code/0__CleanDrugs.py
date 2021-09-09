"""
Automation : 92% success - only 4 out of 49 failed
Automation + Manual : 98% success - only 1 out of 49 failed
Exceptions that failed
Hylo - brand name with not active ingredient?
Estraderm estradiol - Estraderm is the brand name and estradiol active ingredient (corrected manually)
Omega 3 - cleaning program: 3 truncated, also needs hyphen as in omega-3 (corrected manually)
Denosumab 60mg - cleaning program: failed to remove 60mg, space missing (corrected manually)
"""
from csv import reader
project_data = "/home/barnyard/0python/compass/Scraping_and_ETL/data"
f1 = open(project_dir + "0_drugsraw.txt", "r")
f2 = open(project_dir + "0_drugsroot.txt", "w")
rows = list(reader(f1))

drugs=[]

def popit(drug):
    terms = drug.split(' ')
    nolist =['MG','MCG','(ORAL','CHEMO)','(SYMBICORT)','IU','PR','OTC','ML','INHALER','INJECTIONS','COMBINATION']
    for i in range (0,len(nolist)):
        #remove units
        if nolist[i] == terms[-1]:
            terms.remove(terms[-1])
    try:
        #remove numbers
        if float(terms[-1]):
            terms.remove(terms[-1])
    except ValueError:
        False
    #combine list strings
    for c in range(1,len(terms)):
            terms[0] += " " + terms[c]
    return terms[0]

for i in range(0,len(rows)):
    root = rows[i][0] + "\n"
    root = root.replace(" / ", "/").replace(" /", "/")
    min = str.find(root,"/")
    if min < 0:
        drug = [root]
        drug = root.split(' ')
        drug.remove(drug[len(drug)-1])
        for c in range(1,len(drug)):
            drug[0] += " " + drug[c]
        drugs.append(drug[0])
    else:
        drug = root.split('/')
        drug.remove(drug[len(drug)-1])
        for c in range(0,len(drug)):
            drugs.append(drug[c])

#remove units and numbers
print("INPUT")
print(drugs)
print("\n")
for i in range (0,len(drugs)):
    drugs[i] = popit(drugs[i])
    drugs[i] = popit(drugs[i])
    drugs[i] = popit(drugs[i]).lower().capitalize()
#remove duplicates
udrugs = list(set(drugs))
udrugs.sort()

for i in range (0,len(udrugs)):
    line = udrugs[i] + "\n"
    f2.writelines(line)
print("OUTPUT")
print(udrugs)

f2.close()
f1.close()
