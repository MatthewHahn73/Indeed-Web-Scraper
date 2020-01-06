#TODO: Write either a batch script or a subroutine to run the code with specified parameters to auto-run this script
#TODO: Bug: Sometimes duplicates of the same job are sent via sms

import re
import csv
import requests
import argparse
from pyshorteners import Shortener
from pySMS import pySMS
from bs4 import BeautifulSoup    

#URL shortener for better readibility and character limitations 
def Short_Url(url):
	shortener = Shortener('Dagd')
	return shortener.short("http://www." + url)

# Scraping useful data
def Scrap(url, keyWords):
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
	return Vet(jobs, keyWords)

#Vet the list to narrow it down to more reasonable canidates
def Vet(jobList, keyWords):
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
def Main(args):
	totalFound = []
	for a in range(0,3): #Runs search 3 times for redundency
		totalFound.append(Scrap(args.url, args.kwor))
	for b in range(0,len(totalFound),1):
		totalFound[b] = [tuple(lst) for lst in totalFound[b]]
	finalData = sorted(set(totalFound[0]) | set(totalFound[1]) | set(totalFound[2])) 
	if args.csv: #Writes data to a local .csv file
		with open("jobOpenings.csv", "w", newline='') as csvFile:
			write = csv.writer(csvFile)
			for x in range(0, len(finalData)):
				write.writerow([finalData[x][0], 
								'=HYPERLINK("' + finalData[x][1] + '","Application Link")',
								finalData[x][2],
								finalData[x][3]])
			csvFile.close()
	if args.txt: #Writes data to a local .txt
		with open("jobOpenings.txt", "w") as txtFile:
			for x in range(0, len(finalData)):
				txtFile.write("Title: " + finalData[x][0] + "\n" + 
							  "Link: " + Short_Url(finalData[x][1]) + "\n" + 
							  "Company: " + finalData[x][2] + "\n" + 
						      "Date Published: " + finalData[x][3] + "\n\n")
	if args.sms: #Sends data to a number using a provided host email and phone number
		if not (args.ph or args.e or args.p): 
			print("Error; Missing parameter(s)")
		else:	
			smsFinal = "Indeed Job Canidates:\n\n"
			for x in range(0, len(finalData)):
				smsFinal += ("Title: " + finalData[x][0] + "\n" +
							"Link: " + Short_Url(finalData[x][1]) + "\n" + 
							"Company: " + finalData[x][2] + "\n" + 
							"Date Published: " + finalData[x][3] + "\n\n")
			ss = pySMS(str(args.ph), (str(args.e), str(args.p)))
			ss.send("\n" + smsFinal)

#Reads in arguments
if __name__ == "__main__":
	par = argparse.ArgumentParser(description="Indeed Web Scraper v0.5")
	par.add_argument("-url", help="<Required> url argument for web scraper", required=True)
	par.add_argument("-kwor", nargs="+", help="<Required> job title key words", required=True)
	par.add_argument("-csv", help="<Optional> adds info to a local .csv file",
						action="store_true")
	par.add_argument("-txt", help="<Optional> adds info to a local .txt file",
						action="store_true")
	par.add_argument("-sms", help="<Optional> sends data to specified number",
						action="store_true")
	par.add_argument("-ph", help="<Required for SMS> phone number")
	par.add_argument("-e", help="<Required for SMS> host email")
	par.add_argument("-p", help="<Required for SMS> host email password")
	Main(par.parse_args())