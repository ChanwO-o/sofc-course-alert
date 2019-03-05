from flask import *
import websoc, send_sms

app = Flask(__name__)


@app.route("/")
def index():
	coursetuple = websoc.requestCourse(34150)
	print(coursetuple)
	# send_sms.sendMessage(coursetuple)
	return coursetupleToString(coursetuple)

def coursetupleToString(coursetuple):
	result = ''
	for i in coursetuple:
		result += str(i) + '\t'
	return result

if __name__ == "__main__":
	app.run(port=8080)
