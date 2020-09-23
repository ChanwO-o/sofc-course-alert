## **Websoc - UCI Course Alert**

*UC Irvine course availability notification system*

Students can subscribe to any course available in the UC Irvine course system.
When a slot opens for the course, an SMS will be sent to your number with the course code allowing for quick registration!

~~I used this app to my advantage to claim spots earlier than others~~

------------
## **How to use**

1. Download source or clone repo

`git clone https://github.com/ChanwO-o/websoc-coursealert.git`


2. Enter your course codes in the `coursealert.py` file

`COURSECODES = [34170, 34113, 34114, 34190]`


3. Enter phone number to receive SMS in the `send_sms.py` file

`to = "+11234567890"`

------------


Technologies used:
- Python
- Flask
- Twilio SMS API
