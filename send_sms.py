import os
from twilio.rest import Client

account_sid = "AC9d3524428dee9fc80c4088b312020b1e"
auth_token = "ca52852b96d616c75e529ed4ea06045c"

client = Client(account_sid, auth_token)

def sendMessage(coursetuple):
	client.messages.create(
		to = "+13106668374",
		from_= "+12132796150",
		body = "SofC\n" +
		"Course name: " + coursetuple[0] + "\n" +
		"Course code: " + str(123123) + "\n" +
		"Status: " + coursetuple[1]
	)