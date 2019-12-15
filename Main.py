#TODO: Write some code to allow program to run via command line; Include help menu, commands, etc
#TODO: Script command to allow user to pass links via command line 
#TODO: Script command to allow option to output results to .csv files 

import re
import requests
from bs4 import BeautifulSoup

# Scraping useful data
def Scrap(url):
	try:
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
	except Exception as e:
		print(e)
	jobs = []
	for div in soup.find_all(name="div", attrs={"class":"row"}):
		tempJob = []
		for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}): #Job Title/Link
			tempJob.append(a["title"])
			tempJob.append("indeed.com" + a["href"])
		for b in div.find_all("span", attrs={"company"}): #Company Name
			tempJob.append(b.text.strip())
		for c in div.find_all("span", attrs={"class":"date"}): #Date Published
			tempJob.append(c.text.strip())
		for d in div.find_all(class_="location accessible-contrast-color-location"): #Location
			tempJob.append(d.text.strip())
		jobs.append(tempJob)
	r.close()
	return Vet(jobs)

#Vet the list to narrow it down to more reasonable canidates
def Vet(jobList):
	keyWords = ["java", "python", "sql", "c++",
	 "programmer", "junior", "jr", "entry", "intern"]
	newList = []
	iterator = 0
	for eachTitle in [a[0] for a in jobList]: #Narrows based on title keywords
		if any(x in eachTitle.lower() for x in keyWords):
			newList.append(jobList[iterator])
		iterator+=1
	jobList = newList.copy()
	newList.clear()
	iterator = 0
	for eachDate in [a[3] for a in jobList]: #Narrows based on time job posted
		if eachDate.strip() == "Today" or eachDate.strip() == "Just posted":
			newList.append(jobList[iterator])
		else:
			tempInt = int(re.sub('[^0-9]','', eachDate))
			if tempInt < 30:
				newList.append(jobList[iterator])
		iterator+=1
	jobList = newList.copy()
	del newList
	return jobList
		
#Main method
if __name__ == "__main__":
	totalFound = []
	for a in range(0,3):
		totalFound.append(Scrap("https://www.indeed.com/"
			"jobs?q=Programmer&l=Dallas%2C+TX&"
				"limit=30&radius=50&ts=1575602331419&pts="
					"1575374158413&rq=1&rsIdx=0&fromage=last&newcount=291"))
	for b in range(0,len(totalFound),1):
		totalFound[b] = [tuple(lst) for lst in totalFound[b]]
	print(*sorted(set(totalFound[0]) | set(totalFound[1]) | set(totalFound[2])), sep = "\n")