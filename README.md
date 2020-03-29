# Shopping
This app sends text messages about shopping supplies. It allows users to recieve text messages once a supply of their choosing becomes available on some market. 
Auth Code was blocked for security reasons.
The running of this requires the use of ngrok by @inconshreveable, as a server to take in the data recieved from phone texts. 
The app has extensive use of the Twilio API in order to send and recieve text messages. 
The running of this app consists of a few steps:
1. Have python3
2. Have ngrok installed. 
3. Make an account with Twilio (premium account, not trial, strongly reccomended)
4. These are the things that are imported: twilio, tkinter, flask, PIL (pillow). Pip is reccomended for installation if necessary
5. Run command in the directory with the python file and ngrok installation (on UNIX): /ngrok http 5000
- if this fails, run command: sudo lsof -i:5000, and kill the process that appears with command: kill PID
6. Go to the console in Twilio, and see the phone number settings, then copy the first Forwarding address, looks like http://xxxxxxx.ngrok.io, under "a new message comes in"
7. Don't forget to fill in the correct Account SID and Auth Token from the twilio.com/console page. 
8. The app should run with python product2.py. (May need to be python3)
