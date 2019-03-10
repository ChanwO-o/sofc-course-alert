from flask import *
import websoc, send_sms
import threading
import time

app = Flask(__name__)

TIME_BETWEEN_REQUESTS = 3600 # 1 hr
COURSECODES = [34040, 34090, 34150, 34165, 34166, 34167]

@app.route("/")
def index():
	t = threading.Thread(target=startWatchingCourse)
	t.daemon = True # kill thread when main thread dies
	t.start()

	return 'asdf' #coursetupleToString(coursetuple)

def startWatchingCourse():
	while True:
		coursesdata = websoc.requestCourses(COURSECODES)
		print(coursetupleToString(coursesdata))
		# compare contents of coursesdata with database to see changes
		# if status change, send sms
		# send_sms.sendMessage(coursesdata)
		time.sleep(TIME_BETWEEN_REQUESTS) # perform total check every 1 hr
	
def coursetupleToString(coursesdata):
	result = ''
	for i in coursesdata:
		result += str(i) + '\t'
	return result

if __name__ == "__main__":
	app.run(port=8080)
