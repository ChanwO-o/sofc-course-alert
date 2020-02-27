import os
from twilio.rest import Client

account_sid = "AC4021eef031bb9390bfe0bb690aa3418a"
auth_token = "2a9b697ca047a001b2a3e3a079837223"

client = Client(account_sid, auth_token)

def sendMessage(coursesdatalist, verbose=True):
	""" Format text message content with information from coursesdatalist [nameshort, namelong, code, type, max, enroll, waitlist, status]  """
	smsbody = None
	if verbose:
		smsbody = "SofC\n" + constructVerboseBody(coursesdatalist)
	else:
		smsbody = "SofC\n" + constructBody(coursesdatalist)
	client.messages.create(
		to = "+13106668374",
		from_= "+17865653761",
		body = smsbody
	)
	
def constructBody(coursesdatalist):
	""" Construct simple sms body """
	result = ''
	for classtuple in coursesdatalist:
		classinfo = \
		classtuple[0] + " " + str(classtuple[2]) + ' ' + classtuple[7] + "\n."
		result += classinfo
	return result

def constructVerboseBody(coursesdatalist):
	""" Construct verbose sms body """
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