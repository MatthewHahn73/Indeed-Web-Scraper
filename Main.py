#TODO: Write some code to add the option to send data via text (Add subroutine, arguments, etc)

import re
import csv
import requests
import argparse
from bs4 import BeautifulSoup

# Scraping useful data
def Scrap(url):
	try:
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
	except Exception as e:
		print("Error: " + e)
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
def main(args):
	totalFound = []
	for a in range(0,3):
		totalFound.append(Scrap(args.url))
	for b in range(0,len(totalFound),1):
		totalFound[b] = [tuple(lst) for lst in totalFound[b]]
	finalData = sorted(set(totalFound[0]) | set(totalFound[1]) | set(totalFound[2]))
	if args.csv:
		with open("jobOpenings.csv", "w", newline='') as csvFile:
			write = csv.writer(csvFile)
			for x in range(0, len(finalData)):
				write.writerow([finalData[x][0], 
								'=HYPERLINK("' + finalData[x][1] + '","Application Link")',
								finalData[x][2],
								finalData[x][3]])
			csvFile.close()
	if args.txt:
		with open("jobOpenings.txt", "w") as txtFile:
			for x in range(0, len(finalData)):
				txtFile.write("Title: " + finalData[x][0] + "\n" + 
							  "Link: " + finalData[x][1] + "\n" + 
							  "Company: " + finalData[x][2] + "\n" + 
						      "Date Published: " + finalData[x][3] + "\n\n")
	if not args.csv and not args.txt:
		print(*finalData, sep="\n")

#Reads in arguments
if __name__ == "__main__":
	par = argparse.ArgumentParser(description="Indeed Web Scraper v0.2")
	par.add_argument("-csv", help="adds info to a local .csv file",
						action="store_true")
	par.add_argument("-txt", help="adds info to a local .txt file",
						action="store_true")
	par.add_argument("url", help="url argument for web scraper")
	main(par.parse_args())