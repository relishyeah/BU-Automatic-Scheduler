from secret import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from bs4 import BeautifulSoup
import time
import re

class Class:
	def __init__(self,num,room,date,time):
		self.num = num
		self.room = room
		self.date = date
		self.start,self.end = time.split(" ")	

	def __str__(self):
		return self.num + " " + self.room + " " + self.date + " " + self.start + " " + self.end

def makeObjects(x):
	ret = []
	numRegex = re.compile(r"([A-Z]{3})\s([A-Z]{2}\d{3})")
	roomRegex = re.compile(r"([A-Z]{3})\n(\d{3}|[A-Z]{3}|B\d{2})|Arranged")
	timeRegex = re.compile(r"(\d+:\d\dpm|\d+:\d\dam)\n(\d+:\d\dpm|\d+:\d\dam)|Arranged")
	dateRegex = re.compile(r'(Mon|Tue|Wed|Thu|Fri),?(Mon|Tue|Wed|Thu|Fri)?,?(Mon|Tue|Wed|Thu|Fri)?')


	nums = numRegex.findall(x)
	rooms = roomRegex.findall(x)
	dates = dateRegex.findall(x)
	times = timeRegex.findall(x) 


	for i in range(len(nums)):
		ret.append(Class(" ".join(nums[i])," ".join(rooms[i]),"".join(dates[i])," ".join(times[i])))

	return ret


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
