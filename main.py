#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from getpass import getpass
import time,re

from secret import *

class Class:
	def __init__(self,num,room,date,time):
		self.num = num
		self.room = room
		self.date = date
		self.start,self.end = time.split(" ")	

	def __str__(self):
		ret = self.num + " "
		ret += self.room + " " 
		ret += self.start + " " 
		ret += self.end + " "
		for i in range(len(self.date)):
			ret += self.date[i][0] + " "
			ret += self.date[i][1] + " "
		return ret

def convertTime(t):
	ret = []
	l = list(t)
	for i in l:
		t = i.split(":")
		t = [t[0], t[1][:2], t[1][2:]]
		if t[2] == "pm" and t[0]!= "12":
			t[0] = str(int(t[0]) + 12)

		if t[2] == "am":
			if len(t[0]) == 1:
				t[0] = "0" +t[0]
			elif t[0] == "12":
				t[0] = "00"
		t[2] = "00"
		t = ":".join(t)
		ret.append(t)
	return ret

def convertDate(d):
  ret = []
  d = [i for i in d if i]
  days = {'Mon': ["2019-09-09","2019-12-09"]\
  ,'Tue':["2019-09-03","2019-12-10"]\
  ,'Wed':["2019-09-04","2019-12-11"]\
  ,'Thu':["2019-09-05","2019-12-05"]\
  ,'Fri':["2019-09-06","2019-12-06"]  }
  
  for day in d:
    ret.append(days[day])
  
  return ret

def makeObjects(x):
	ret = []
	numRegex = re.compile(r"([A-Z]{3})\s([A-Z]{2}\d{3})")
	roomRegex = re.compile(r"([A-Z]{3})\n(\d{3}|[A-Z]{3}|B\d{2})|Arranged")
	timeRegex = re.compile(r"(\d+:\d\dpm|\d+:\d\dam)\n(\d+:\d\dpm|\d+:\d\dam)|Arranged")
	dateRegex = re.compile(r'(Mon|Tue|Wed|Thu|Fri),?(Mon|Tue|Wed|Thu|Fri)?,?(Mon|Tue|Wed|Thu|Fri)?|Arranged')


	nums = 	numRegex.findall(x)
	rooms = roomRegex.findall(x)
	dates = dateRegex.findall(x)
	times = timeRegex.findall(x) 

	print(dates)

	for i in range(len(nums)):
		ret.append(Class(" ".join(nums[i])," ".join(rooms[i]),(convertDate(dates[i]))," ".join(convertTime(times[i]))))

	return ret

def run():
	#username = input("BU alias")
	#password = getpass()

	browser = webdriver.Chrome(r"C:\Users\quinn\Dropbox\Personal Projects\webdriver\chromedriver.exe")
	browser.get("https://www.bu.edu/studentlink")

	html = browser.find_element_by_xpath("/html/body/center[1]/table[4]/tbody/tr/td[1]/table/tbody/tr[1]/td/a/img")
	html.click()

	html = browser.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/table/tbody/tr/td/font/a[8]")
	html.click()	


	u_field = browser.find_element_by_id('j_username')
	u_field.send_keys(username)

	p_field = browser.find_element_by_id('j_password')
	p_field.send_keys(password)
	p_field.send_keys(Keys.RETURN)

	time.sleep(3)
	html = browser.page_source
	soup = BeautifulSoup(html,"html.parser")

	for script in soup(["script", "style"]):
	    script.extract() 

	text = soup.get_text()
	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = '\n'.join(chunk for chunk in chunks if chunk)
	text = text.split("Print")[1]
	text = text.split("Total Credits")[0]

	browser.close()
	for i in makeObjects(text):
		print(i)   

run()