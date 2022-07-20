from array import array
from bs4 import BeautifulSoup
import requests
from collections import defaultdict

site= "https://bw11.clpccd.cc.ca.us/clpccd/2022/02/l/sched_cs.htm"
hdr = {'User-Agent': 'Mozilla/5.0'}

page = requests.get(site, headers=hdr)
soup = BeautifulSoup(page.content, 'html.parser')
# changed to not be hardcoded
tableBody = soup.find("body").find("table", border="1", cellspacing="0", cellpadding="2", width="100%").find_all("tr")
data = []

tempStorage = []
categories = []

for table in list(tableBody):
	categories = []
	for tableRow in list(table):
		trt = tableRow.get_text().strip()
		if(u'\xa0\n' in trt):
			if(trt[0:6] == "ONLINE"):
				categories.append("ONLINE")
			else:
				categories.append(trt[0:4].strip())
		elif(not trt or len(trt)>50 or trt == "View textbooks"):
			continue
		elif(trt):
			categories.append(trt)
	tempStorage.append(categories)

oneDict = {}
headers1 = list(map(lambda x: x.replace(" ", ""), tempStorage[1]))
headers2 = list(map(lambda x: x.replace(" ", ""), tempStorage[2]))
checkMain = False
scheduleData = []
for row in tempStorage[3:]:
	if(row == []):
		checkMain = False
		if(oneDict):
			oneDict["Schedule"] = (scheduleData)
		scheduleData = []
		data.append(oneDict)
		oneDict = {}
	
	elif(checkMain == False):
		for i in range(len(headers1)):
			oneDict[headers1[i]] = (row[i])
		checkMain = True
	
	elif("Instructor(s):" in row[0]):
		instructor = row[0].replace("Instructor(s): ","")
		if("GENERAL" not in instructor):
			instructor = " ".join(list(map(lambda x : x[0]+(x[1:].lower()), instructor.split(" "))))
		oneDict["Instructor"] = instructor
	else:
		scheduleDict = {}
		if(row[2] == "-"):
			scheduleDict["StartDate"] = row[0]
			scheduleDict["EndDate"] = row[1]
			scheduleDict["Days"] = "Async"
			scheduleDict["Times"] = "Async"
			scheduleDict["Room"] = "ONLINE"
			scheduleDict["Bldg"] = "ONLINE"
		else:
			for i in range(len(headers2)):
				if(row[i] == "MW"): row[i] = "Monday and Wednesday"
				elif(row[i] == "TTh"): row[i] = "Tuesday and Thursday"
				elif(row[i] == "T"): row[i] = "Tuesday"
				elif(row[i] == "Th"): row[i] = "Thursday"
				elif(row[i] == "W"): row[i] = "Wednesday"
				elif(row[i] == "M"): row[i] = "Monday"
				scheduleDict[headers2[i]] = (row[i])
		scheduleData.append(scheduleDict)


data = list(filter(lambda x:x != {}, data))

	