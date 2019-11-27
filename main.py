#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from getpass import getpass
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle,re,time

scopes = ["https://www.googleapis.com/auth/calendar"]

try:
	credentials = pickle.load(open("token.pkl", "rb"))
except:
	flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes=scopes)
	credentials = flow.run_console()
	pickle.dump(credentials, open("token.pkl", "wb"))

service = build("calendar", "v3", credentials=credentials)
result = service.calendarList().list().execute()
calender_id = result['items'][0]['id']

def makeEvent(c):
    event = {
        'summary' : c.num,
        'location' : c.room,
        'start': {'dateTime': c.date + 'T' + c.start + '-05:00',
        'timeZone' : "America/New_York"},
        'end': {'dateTime': c.date + 'T' + c.end + '-05:00',
        'timeZone' : "America/New_York"},
        "recurrence": [
            "RRULE:FREQ=WEEKLY;UNTIL=20191212;BYDAY=" + ",".join(c.dow)
        ]
    }

    event =service.events().insert(calendarId = calender_id, body = event).execute()
    print(str(c.num),"Created")

class Class:
	def __init__(self,num,room,date,time):
		self.num = num
		self.room = room
		self.date = date[1]
		self.dow = date[0]

		self.start,self.end = time.split(" ")	

	def __str__(self):
		ret = self.num + " "
		ret += self.room + " " 
		ret += self.start + " " 
		ret += self.end + " "

		for i in self.dow:
			ret +=(i) + " "

		ret += self.date
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
  d = [i[:2].upper() for i in d if i]

  ret.append(d)
  days = {'MO': "2019-09-09"\
  ,'TU':"2019-09-03"\
  ,'WE':"2019-09-04"\
  ,'TH':"2019-09-05"\
  ,'FR':"2019-09-06"  }
  
  ret.append(days[d[0]])
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

	for i in range(len(nums)):
		ret.append(Class(" ".join(nums[i])," ".join(rooms[i]),(convertDate(dates[i]))," ".join(convertTime(times[i]))))

	return ret

def run():
	username = input("BU alias ")
	password = getpass()

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
		makeEvent(i)   

run()