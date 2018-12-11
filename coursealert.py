from flask import *
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
URL = 'https://www.reg.uci.edu/perl/WebSoc'

DATA = 'Submit=Display+Web+Results&YearTerm=2019-03&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=+ALL&CourseNum=&Division=ANY&CourseCodes=34140&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='

@app.route("/")
def index():
	response = requests.post(url = URL, data = DATA)
	return processResponseString(response)



def processResponseString(response):
	rtext = response.text

	
	soup = BeautifulSoup(rtext, 'html.parser')
	allfonttags = soup.findAll('font') # returns list of html elements
	
	
	if len(allfonttags) == 0:
		return 'ERROR no courses found'
	elif len(allfonttags) == 2: # will return list of length 2 only if course is FULL
		return str(allfonttags[0]) + '	' + 'FULL'
	elif len(allfonttags) == 3: # course is OPEN or Waitl
		return str(allfonttags[0]) + '	' + str(allfonttags[1])
	
	
if __name__ == "__main__":  
    app.run(port=8080)
