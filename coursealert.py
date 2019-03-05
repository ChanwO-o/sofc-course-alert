from flask import *
import requests
import websoc, send_sms

app = Flask(__name__)
URL = 'https://www.reg.uci.edu/perl/WebSoc'


@app.route("/")
def index():
	response = requests.post(url = URL, data = websoc.DATA)
	coursetuple = websoc.processResponse(response)
	# send_sms.sendMessage(coursetuple)
	return 'asdf'


if __name__ == "__main__":
	app.run(port=8080)
