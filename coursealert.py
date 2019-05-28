from flask import *
import websoc, send_sms
import threading
import time

app = Flask(__name__)

TIME_BETWEEN_REQUESTS = 6
COURSECODES = [34170, 34113, 34114, 34190]
# 34170: 147 iot
# 34113, 34114: 134 better discussion
# 34190: 161 lec

@app.route("/")
def index():
	t = threading.Thread(target=startWatchingCourse)
	t.daemon = True # kill thread when main thread dies
	t.start()

	return 'running...'

def startWatchingCourse():
	while True:
		coursesdatalist = websoc.requestCourses(COURSECODES)
		print(coursesdataToString(coursesdatalist))
		# ULTIMATE GOAL: compare contents of coursesdatalist with database to see changes
		# if status change, send sms
		# for now, just text all OPEN classes
		openclasses = []
		for classtuple in coursesdatalist:
			if classtuple[-1] != 'FULL':
				openclasses.append(classtuple)

		# send_sms.sendMessage(coursesdatalist, verbose=False) # option 1: text entire class list
		
		if len(openclasses) > 0:
			print(openclasses)
			send_sms.sendMessage(openclasses, verbose=False) # option 2: text open classes only (if there are any)
		
		time.sleep(TIME_BETWEEN_REQUESTS) # perform total check every 5 minutes
	
def coursesdataToString(coursesdatalist):
	result = ''
	for i in coursesdatalist:
		result += str(i) + '\t'
	return result

if __name__ == "__main__":
	app.run(port=8080)
