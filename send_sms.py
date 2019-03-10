import os
from twilio.rest import Client

account_sid = "AC9d3524428dee9fc80c4088b312020b1e"
auth_token = "ca52852b96d616c75e529ed4ea06045c"

client = Client(account_sid, auth_token)

def sendMessage(coursesdatalist):
	""" Format text message content with information from coursesdatalist [nameshort, namelong, code, type, max, enroll, waitlist, status]  """
	client.messages.create(
		to = "+13106668374",
		from_= "+12132796150",
		body = "SofC\n" + constructBody(coursesdatalist)
	)
	
def constructBody(coursesdatalist):
	result = ''
	for classtuple in coursesdatalist:
		classinfo = \
		"\nCourse name: " + classtuple[0] + " " + classtuple[1] + "\n" +\
		"Code: " + str(classtuple[2]) + "\n" +\
		"Type: " + classtuple[3] + "\n" +\
		"Max: " + classtuple[4] + "\n" +\
		"Enrolled: " + classtuple[5] + "\n" +\
		"Waitlist: " + classtuple[6] + "\n" +\
		"Status: " + classtuple[7] + "\n."
		result += classinfo
	return result