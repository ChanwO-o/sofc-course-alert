from flask import *
import websoc, send_sms
import threading
import time

app = Flask(__name__)


@app.route("/")
def index():
	t = threading.Thread(target=startWatchingCourse)
	t.daemon = True
	t.start()
	
	'''
	coursetuple = websoc.requestCourse(34150)
	print(coursetuple)
	# send_sms.sendMessage(coursetuple)
	'''
	
	return 'asdf' #coursetupleToString(coursetuple)

def startWatchingCourse():
	while True:
		time.sleep(5)
		print('sleep')
	
def coursetupleToString(coursetuple):
	result = ''
	for i in coursetuple:
		result += str(i) + '\t'
	return result

if __name__ == "__main__":
	app.run(port=8080)
