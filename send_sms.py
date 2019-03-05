import os
from twilio.rest import Client

account_sid = "AC9d3524428dee9fc80c4088b312020b1e"
auth_token = "ca52852b96d616c75e529ed4ea06045c"

client = Client(account_sid, auth_token)

def sendMessage(coursetuple):
	""" Format text message content with information from coursetuple (name, code, type, max, enroll, waitlist, status)  """
	client.messages.create(
		to = "+13106668374",
		from_= "+12132796150",
		body = "SofC\n" +
		"Course name: " + coursetuple[0] + "\n" +
		"Code: " + str(coursetuple[1]) + "\n" +
		"Type: " + coursetuple[2] + "\n" +
		"Max: " + coursetuple[3] + "\n" +
		"Enrolled: " + coursetuple[4] + "\n" +
		"Waitlist: " + coursetuple[5] + "\n" +
		"Status: " + coursetuple[6]
	)