
"""
For running on Linux machine,
change 

import requests
import urllib.request as urllib2

to

import urllib2
"""

import requests
import urllib.request as urllib2
from lxml import html
from bs4 import BeautifulSoup
import json 

#Globals
RECENT = 0
PAST = 1
WIKI = 'https://www.hackerearth.com/jobs/hiring/'

def GetPageSource():
	page = urllib2.urlopen(WIKI)
	soup = BeautifulSoup(page, "lxml")
	return soup

def SeparateRecentAndPastLists(soup):
	lists = soup.find_all("div", class_="jobs-list")
	return lists
	

def FindJobs(lists, listnum):
	jobs = lists[listnum].find_all("div", class_="content job-container show-hover")	
	return jobs

def GetCompanyName(job):
	company_name = (job.find("div", class_="less-margin body-font company-title"))
	return str(company_name.find(class_="dark").get_text())[:-1]

def GetWorkLocation(job):	
	details = job.find_all("div", class_="float-left standard-margin-right")
	return str(details[0].get_text())[1:]

def GetExperience(job):	
	details = job.find_all("div", class_="float-left standard-margin-right")
	return details[1].get_text()

def GetSalary(job):	
	details = job.find_all("div", class_="float-left standard-margin-right")
	return str(details[2].get_text())[1:]
	
def GetSkillsList(job):
	skills_list = []
	skills = job.find("div", class_="less-margin job-skills body-font")
		
	if skills is not None:
		skills = skills.find_all("div", class_="nice-tag")
		for skill in skills:
			skills_list.append(skill.get_text())
			
	return skills_list
	
def GetMinimumExperience(experience):
	return int(str((str(experience).split("-"))[0])[13:])
	
def GetMaximumExperience(experience):
	return int(str((str(experience).split("-"))[len(str(experience).split("-"))-1])[:-10])
	
def GetLink(job):
	base = "www.hackerearth.com"
	link = job.a["href"]
	return base + link
	
def DifferentiateEachJob(jobs):
	list_of_jobs = []
	for job in jobs:
		job_object = {}
		company_name = GetCompanyName(job)
		job_object["company_name"] = company_name
		work_location = GetWorkLocation(job)
		job_object["work_location"] = work_location
		experience = GetExperience(job)
		minimum_experience = GetMinimumExperience(experience)
		maximum_experience = GetMaximumExperience(experience)
		job_object["minimum_experience"] = minimum_experience
		job_object["maximum_experience"] = maximum_experience
		salary = GetSalary(job)
		job_object["Salary"] = str(salary)[6:]
		skills_list = GetSkillsList(job)
		job_object["skills"] = skills_list
		link = GetLink(job)
		job_object["link"] = link
		#print(company_name, work_location, experience, salary, skills_list)
		list_of_jobs.append(job_object)
	#print("\n\n\n")
	json_object = json.dumps(list_of_jobs)
	print(json.dumps(json.loads(json_object), indent = 4, sort_keys = True))
		
soup = GetPageSource()
lists = SeparateRecentAndPastLists(soup)
latest_jobs = FindJobs(lists, RECENT)
DifferentiateEachJob(latest_jobs)
