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
	coursesdata = processResponse(response, codes)
	return coursesdata

def processResponse(response, codes):
	""" Return a list of tuples with information on courses. In the form of (name, code, type, max, enroll, waitlist, status)  """
	rtext = response.text
	soup = BeautifulSoup(rtext, 'html.parser')
	
	# filter out no results
	allfonttags = soup.findAll('font')
	if len(allfonttags) == 0:
		print('ERROR no courses found')
		return tuple('ERROR no courses found')
	
	resultclasses = []
	courseshtmlblocks = splitHtmlByCourse(soup) # first split html by course
	for coursehtmlblock in courseshtmlblocks:
		soup = BeautifulSoup(coursehtmlblock, 'html.parser') # soup = course block
		cnameshort = getCourseNameShort(soup)
		cnamelong = getCourseNameLong(soup)
		
		classtrblocks = splitHtmlByClass(soup) # now split html by individual class (may contain multiple classes)
		print('Number of classes found for course:', str(len(classtrblocks)))
		for trblock in classtrblocks:
			classinfolist = trblock.findAll('td')
			ccode = getClassCode(classinfolist)
			ctype = getClassType(classinfolist)
			cmax = getClassMax(classinfolist)
			cenroll = getClassEnroll(classinfolist)
			cwaitlist = getClassWaitlist(classinfolist)
			cstatus = getClassStatus(classinfolist)
			classtuple = (cnameshort, cnamelong, ccode, ctype, cmax, cenroll, cwaitlist, cstatus)
			resultclasses.append(classtuple)

	return resultclasses
	
def splitHtmlByCourse(soup):
	""" Split html into big chunks by course & returned as a list (e.g. ICS46) """
	courses = soup.prettify().split('<tr bgcolor="#fff0ff" valign="top">') # start of every <tr> tag that declares course name
	return courses[1:len(courses)]
	
def splitHtmlByClass(soup):
	"""
	Find all <tr> blocks that represent a class & return as a list (all requested lec, dis, lab1, lab2 under one course)
	If multiple classes are searched for one course (e.g. two lab sessions), websoc returns these classes as rows under one table.
	Each row is a <tr> block with an alternating background color between '#FFFFCC' and 'DDEEFF'.
	Some classes return more <tr> blocks with the same bgcolor, but the distinct leading <tr> block also has the valign="top" attribute attached as well.
	"""
	firstcolor = soup.findAll('tr', {'bgcolor' : '#FFFFCC', 'valign' : 'top'})
	secondcolor = soup.findAll('tr', {'bgcolor' : '#DDEEFF', 'valign' : 'top'})
	return firstcolor + secondcolor # return extended list
	
def getCourseNameShort(soup):
	""" Extract course short name from response (e.g. ICS 46) """
	return soup.find('td', {'class' : 'CourseTitle'}).text.split('\n')[1].strip().encode('ascii', 'ignore').decode('utf-8')
	
def getCourseNameLong(soup):
	""" Extract course long name from response (e.g. DATA STRC IMPL&ANLS) """
	return soup.find('b').text.strip() # tr tag with bgcolor -> get bold tag -> text
	
def getClassCode(classinfolist):
	""" Extract class code from response """
	return classinfolist[0].text.strip() # first td tag
	
def getClassType(classinfolist):
	""" Extract class type from response (lec, dis, lab, etc) """
	return classinfolist[1].text.strip() # second td tag

def getClassMax(classinfolist):
	""" Extract class max count from response """
	return classinfolist[8].text.strip() # ninth td tag

def getClassEnroll(classinfolist):
	""" Extract class enroll count from response """
	return classinfolist[9].text.strip()

def getClassWaitlist(classinfolist):
	""" Extract class waitlist count from response """
	return classinfolist[10].text.strip()

def getClassStatus(classinfolist):
	""" Extract class status from response """
	return classinfolist[16].text.strip()