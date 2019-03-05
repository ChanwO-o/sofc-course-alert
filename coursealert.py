from flask import *
import websoc, send_sms

app = Flask(__name__)


@app.route("/")
def index():
	websoc.requestCourse(34150)
	# send_sms.sendMessage(coursetuple)
	return 'asdf'


if __name__ == "__main__":
	app.run(port=8080)
