from flask import *
import websoc, send_sms
import threading
import time

app = Flask(__name__)

TIME_BETWEEN_REQUESTS = 300 #3600 # 1 hr
COURSECODES = [34040, 34090, 34150, 34165, 34166, 34167]#[383, 34090]#

@app.route("/")
def index():
	t = threading.Thread(target=startWatchingCourse)
	t.daemon = True # kill thread when main thread dies
	t.start()

	return 'running...'

def startWatchingCourse():
	while True:
		coursesdatalist = websoc.requestCourses(COURSECODES)
		# print(coursesdataToString(coursesdatalist))
		# compare contents of coursesdatalist with database to see changes
		# if status change, send sms
		send_sms.sendMessage(coursesdatalist, verbose=False)
		time.sleep(TIME_BETWEEN_REQUESTS) # perform total check every 1 hr
	
def coursesdataToString(coursesdatalist):
	result = ''
	for i in coursesdatalist:
		result += str(i) + '\t'
	return result

if __name__ == "__main__":
	app.run(port=8080)
