import requests
from bs4 import BeautifulSoup

URL = 'https://www.reg.uci.edu/perl/WebSoc'

def constructRequestString(codes : [int]):
	""" Construct the string to pass to websoc request """
	return'Submit=Display+Web+Results&YearTerm=2019-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=+ALL&CourseNum=&Division=ANY&CourseCodes=' + constructCourseCodeString(codes) + '&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room='

	'''	Submit=Display+Web+Results&YearTerm=2019-14&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=+ALL&CourseNum=&Division=ANY&CourseCodes=34040+34090+34150&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room=
	'''
	
def constructCourseCodeString(codes : [int]):
	""" Construct course code portion of request string in the form of 34040+34090+34150 """
	if len(codes) == 0:
		return None
	if len(codes) == 1:
		return str(codes[0])
	result = str(codes[0])
	for i in range(1, len(codes)):
		result += '+' + str(codes[i])
	return result
	
def requestCourses(codes):
	""" Make request for information on course by provided course codes """
	response = requests.post(url = URL, data = constructRequestString(codes))
	coursetuple = processResponse(response, codes)
	return coursetuple

def processResponse(response, codes):
	""" Return a list of tuples with information on courses. In the form of (name, code, type, max, enroll, waitlist, status)  """
	rtext = response.text
	soup = BeautifulSoup(rtext, 'html.parser')
	
	# filter out no results
	allfonttags = soup.findAll('font')
	if len(allfonttags) == 0:
		print('ERROR no courses found')
		return tuple('ERROR no courses found')
	
	courseshtmlblocks = splitHtmlByCourse(soup) # list of html blocks per course
	
	result = []
	for htmlblock in courseshtmlblocks:
		soup = BeautifulSoup(htmlblock, 'html.parser')
		cname = getCourseName(soup)
		ctype = getCourseType(soup)
		cmax = getCourseMax(soup)
		cenroll = getCourseEnroll(soup)
		cwaitlist = getCourseWaitlist(soup)
		cstatus = getCourseStatus(soup)
		print((cname, ctype, cmax, cenroll, cwaitlist, cstatus))
	return result
	
def splitHtmlByCourse(soup):
	""" Split html into blocks by course & returned as a list """
	courses = soup.prettify().split('<tr bgcolor="#fff0ff" valign="top">') # start of every <tr> tag that declares course name
	return courses[1:len(courses)]
	
def getCourseName(soup):
	""" Extract name from response """
	return soup.find('b').text # tr tag with bgcolor -> get bold tag -> text
	
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