from flask import *
import websoc, send_sms
import threading
import time

app = Flask(__name__)

TIME_BETWEEN_REQUESTS = 300 #3600 # 1 hr
COURSECODES = [36452,34160,36451,36452,36453,36454,36455,36456] # 34165, 34166, 34167, 34168, 34169, 34170, 34171, 34172] #34150, 36451, 36452, 36453, 36454, 36455, 36456] #[34040, 34090, 34150, 34165, 34166, 34167]#[383, 34090]#
#36452 34160 36451 36452 36453 36454 36455 36456

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
		
		# for now, just text OPEN classes only
		openclasses = []
		for classtuple in coursesdatalist:
			if classtuple[-1] == 'OPEN':
				openclasses.append(classtuple)

		send_sms.sendMessage(coursesdatalist, verbose=False) # text entire class list
		send_sms.sendMessage(openclasses, verbose=False) # text open classes only
		
		time.sleep(TIME_BETWEEN_REQUESTS) # perform total check every 5 minutes
	
def coursesdataToString(coursesdatalist):
	result = ''
	for i in coursesdatalist:
		result += str(i) + '\t'
	return result

if __name__ == "__main__":
	app.run(port=8080)
