import os
from twilio.rest import Client

account_sid = "AC9d3524428dee9fc80c4088b312020b1e"
auth_token = "ca52852b96d616c75e529ed4ea06045c"

client = Client(account_sid, auth_token)

client.messages.create(
	to="+13106668374",
	from_="+12132796150",
	body="This is the ship that made the Kessel Run in twelve parsecs?"
)