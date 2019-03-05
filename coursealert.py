from flask import *
import websoc, send_sms
import threading
import time

app = Flask(__name__)

TIME_BETWEEN_REQUESTS = 60 # 1 min
TIME_BETWEEN_CHECKS = 3600 # 1 hr
COURSECODES = [34040, 34090, 34150, 34165, 34166, 34167]

@app.route("/")
def index():
	t = threading.Thread(target=startWatchingCourse)
	t.daemon = True
	t.start()

	return 'asdf' #coursetupleToString(coursetuple)

def startWatchingCourse():
	while True:
		for code in COURSECODES:
			coursetuple = websoc.requestCourse(code)
			print(coursetupleToString(coursetuple))
			# compare contents of coursetuple with database to see changes
			# if status change, send sms
			send_sms.sendMessage(coursetuple)
			time.sleep(TIME_BETWEEN_REQUESTS) # distance each course request by 1 min
		time.sleep(TIME_BETWEEN_CHECKS) # perform total check every 1 hr
	
def coursetupleToString(coursetuple):
	result = ''
	for i in coursetuple:
		result += str(i) + '\t'
	return result

if __name__ == "__main__":
	app.run(port=8080)
