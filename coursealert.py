from flask import *
import requests
from bs4 import BeautifulSoup
import send_sms

app = Flask(__name__)
URL = 'https://www.reg.uci.edu/perl/WebSoc'

DATA = 'Submit=Display+Web+Results&YearTerm=2019-03&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=+ALL&CourseNum=&Division=ANY&CourseCodes=34140&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='

@app.route("/")
def index():
	response = requests.post(url = URL, data = DATA)
	coursetuple = processResponseString(response)
	send_sms.sendMessage(coursetuple)
	return coursetuple


def processResponseString(response):
	rtext = response.text

	
	soup = BeautifulSoup(rtext, 'html.parser')
	allfonttags = soup.findAll('font') # returns list of html elements
	
	
	if len(allfonttags) == 0:
		return tuple('ERROR no courses found')
	elif len(allfonttags) == 2: # will return list of length 2 only if course is FULL
		return tuple((allfonttags[0].getText(), 'FULL'))
	elif len(allfonttags) == 3: # course is OPEN or Waitl
		return tuple((allfonttags[0].getText(), allfonttags[1].getText()))
	
	
if __name__ == "__main__":  
    app.run(port=8080)
