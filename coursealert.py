from flask import *
import requests
from bs4 import BeautifulSoup
import send_sms

app = Flask(__name__)
URL = 'https://www.reg.uci.edu/perl/WebSoc'

DATA = 'Submit=Display+Web+Results&YearTerm=2019-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=+ALL&CourseNum=&Division=ANY&CourseCodes=341630&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='

@app.route("/")
def index():
	response = requests.post(url = URL, data = DATA)
	coursetuple = processResponseString(response)
	# send_sms.sendMessage(coursetuple)
	return 'asdf'


def processResponseString(response):
	""" Return a tuple with information on course. In the form of (name, code, type, enrcount, waitlist, status)  """
	rtext = response.text
	soup = BeautifulSoup(rtext, 'html.parser')
	
	# filter out no results
	allfonttags = soup.findAll('font')
	if len(allfonttags) == 0:
		print('ERROR no courses found')
		return tuple('ERROR no courses found')
	
	name = getCourseName(soup)
	print(name)
	
	
	# elif len(allfonttags) == 2: # will return list of length 2 only if course is FULL
		# return tuple((allfonttags[0].getText(), 'FULL'))
	# elif len(allfonttags) == 3: # course is OPEN or Waitl
		# return tuple((allfonttags[0].getText(), allfonttags[1].getText()))
	
def getCourseName(soup):
	""" Extract name from response """
	return soup.find('tr', {'bgcolor' : '#fff0ff'}).find('b').text # tr tag with bgcolor -> get bold tag -> text
	
	
if __name__ == "__main__":  
    app.run(port=8080)
