from flask import *
import requests

app = Flask(__name__)
URL = 'https://www.reg.uci.edu/perl/WebSoc'

DATA = 'Submit=Display+Web+Results&YearTerm=2019-03&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=+ALL&CourseNum=&Division=ANY&CourseCodes=34130&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='

@app.route("/")
def index():
	response = requests.post(url = URL, data = DATA)
	return processResponseString(response)
	


def processResponseString(response):
	rtext = response.text
	if ("No courses matched your search criteria for this term." in rtext) or ("Error:" in rtext):
		return "ERROR"
	
	index = rtext.find('</font></td></tr>')
	indexstart = index - 6
	return rtext[indexstart : indexstart + 6]
	#return rtext
	
	
if __name__ == "__main__":  
    app.run(port=8080)
