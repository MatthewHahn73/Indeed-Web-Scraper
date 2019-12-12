#TODO: Write some code to autorun this script
#TODO: Potential bug: Scraping yeilds significantly varying results (Related to vetting process?)

import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver

# Scraping useful data
def Scrap(url):
	try:
		driver = webdriver.Chrome()
		driver.get(url)
		soup = BeautifulSoup(driver.page_source, "html.parser")
		time.sleep(3)
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
	driver.close()
	return jobs

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
		if eachDate.strip() == "Today":
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
	vettedList = Vet(Scrap("https://www.indeed.com/"
			"jobs?q=Programmer&l=Dallas%2C+TX&"
				"limit=30&radius=50&ts=1575602331419&pts="
					"1575374158413&rq=1&rsIdx=0&fromage=last&newcount=291"))
	print(*vettedList, sep = "\n")