import requests
from bs4 import BeautifulSoup

URL = 'https://www.reg.uci.edu/perl/WebSoc'

def constructRequestString(code):
	""" Construct the string to pass to websoc request """
	return'Submit=Display+Web+Results&YearTerm=2019-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=+ALL&CourseNum=&Division=ANY&CourseCodes=' + str(code) + '&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='

def requestCourse(code):
	""" Make request for information on course by provided course code """
	response = requests.post(url = URL, data = constructRequestString(code))
	coursetuple = processResponse(response)
	return coursetuple

def processResponse(response):
	""" Return a tuple with information on course. In the form of (name, code, type, max, enroll, waitlist, status)  """
	rtext = response.text
	soup = BeautifulSoup(rtext, 'html.parser')
	
	# filter out no results
	allfonttags = soup.findAll('font')
	if len(allfonttags) == 0:
		print('ERROR no courses found')
		return tuple('ERROR no courses found')
	
	name = getCourseName(soup)
	type = getCourseType(soup)
	max = getCourseMax(soup)
	enroll = getCourseEnroll(soup)
	waitlist = getCourseWaitlist(soup)
	status = getCourseStatus(soup)
	return(name, type, max, enroll, waitlist, status)
	
def getCourseName(soup):
	""" Extract name from response """
	return soup.find('tr', {'bgcolor' : '#fff0ff'}).find('b').text # tr tag with bgcolor -> get bold tag -> text

def getCourseType(soup):
	""" Extract course type from response (lec, dis, lab, etc) """
	return soup.find('tr', {'bgcolor' : '#FFFFCC'}).findAll('td')[1].text # tr tag with bgcolor -> get second td tag -> text

def getCourseMax(soup):
	""" Extract course max count from response """
	return soup.find('tr', {'bgcolor' : '#FFFFCC'}).findAll('td')[8].text # tr tag with bgcolor -> get ninth td tag -> text

def getCourseEnroll(soup):
	""" Extract course enroll count from response """
	return soup.find('tr', {'bgcolor' : '#FFFFCC'}).findAll('td')[9].text

def getCourseWaitlist(soup):
	""" Extract course waitlist count from response """
	return soup.find('tr', {'bgcolor' : '#FFFFCC'}).findAll('td')[10].text

def getCourseStatus(soup):
	""" Extract course status from response """
	return soup.find('tr', {'bgcolor' : '#FFFFCC'}).findAll('td')[16].text