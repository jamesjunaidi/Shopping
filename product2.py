from twilio.rest import Client
#from server import *
import tkinter
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

#import server.py

listOfTPnumbers = []
listOfHSnumbers = []
listOfNumbers = []

numOfTimesRan = 0
app = Flask(__name__)
#app.run(debug=True)

TPText = open("TPnumbers.txt", "w+")


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    global numOfTimesRan
    numOfTimesRan += 1
    print("incoming_sms() has ran this many times:" + str(numOfTimesRan))
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    number = request.values.get('From', None)

    # Start our TwiML response
    resp = MessagingResponse()
    global listOfTPnumbers
    global listOfHSnumbers
    global listOfNumbers
    if body == '1':
        
        if number not in listOfTPnumbers:
            listOfTPnumbers.append(number)
            TPText.write("%s\n" % number)
            resp.message("We will text you when toilet paper is available")
        else:
            resp.message("You are already subscribed to toilet paper notifications")
    elif body == '2':
        if number not in listOfHSnumbers:
            listOfHSnumbers.append(number)
            resp.message("We will text you when hand sanitizer is available")
        else:
            resp.message("You are already subscribed to hand sanitizer notifications")
    else:
        resp.message("You are enrolled in Solomon James Rushil inventory service. To buy toilet paper, text 1. To buy hand saniter, text 2.")
        if number not in listOfNumbers:
            listOfNumbers.append(number)
    
    print("printing the TP array")
    for item in listOfTPnumbers:
        print(item)
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
#global string var
itemString = ""

TPText.close()

#grabs input from the first Entry (item) (This might be useless now)
# def retrieve_input():
#     print("Input: %s\n" % (e1.get()))
#     return str(e1.get())

#grabs input from the second Entry (quantity)    
def retrieve_quantity():
    return str(e2.get())
def retrieve_store():
    return str(eL.get())

    
#start twilio

# Your Account SID from twilio.com/console
account_sid = "ACf21b270aa57d4c7ce089f2ca9d472e90"
# Your Auth Token from twilio.com/console
auth_token = "XXXX"

client = Client(account_sid, auth_token)

def sendMessage():
    print("got to sendMessage")
    #this var will hold the complteted string
    string = "The item " + itemString + " is now in stock in " + retrieve_store() + "." + " There are " + retrieve_quantity() + " available."
    #this line actually sends the message
    #message = client.messages.create(to="+19163657393", from_="+16178198883", body=string)
    if itemString == "Toilet Paper": 
        print("got to send Toilet Paper")
        with open("TPnumbers.txt", "r+") as filehandle:
            for number in filehandle:
                print("got to for each number")
                message = client.messages.create(to= number, from_="+16178198883", body=string)
    if itemString == "Hand Sanitizer":
        for number in listOfHSnumbers:
            message = client.messages.create(to= number, from_="+16178198883", body=string)

#start GUI
#retrieve input from the text boxes:


m=tkinter.Tk() #m is the name of the main window object
m.geometry('725x500')
m.title("LA Hacks 2020")

storeLabel = tkinter.Label(m, text="Enter your store here")
storeLabel.pack()
#eL will contain the item that is available
eL = tkinter.Entry(m)
eL.pack()

label1 = tkinter.Label(m, text="Input item here")
label1.pack()

#itemList will contain the item that is available
def toiletClick():
    print("Toilet ran")
    global itemString
    itemString = "Toilet Paper"
    print("should be array above")
 
toiletPaperButton = tkinter.Radiobutton(m, text = "Toilet Paper", value = 1, command = toiletClick)
toiletPaperButton.pack()

def handSantizerClick():
    print("santizer ran")
    global itemString
    itemString = "Hand Sanitizer"
    print(itemString)
    
handSanitizerButton = tkinter.Radiobutton(m, text = "Hand Sanitizer", value = 0, command = handSantizerClick)
handSanitizerButton.pack()


label2 = tkinter.Label(m, text="Input quantity of item here")
label2.pack()
#e2 contains the quantity of the item
e2 = tkinter.Entry(m)
e2.pack()

getButton = tkinter.Button(m, text="send message entered", width=35, command=sendMessage)
getButton.pack()

button = tkinter.Button(m, text="close window", width=25, command=m.destroy)
button.pack()

m.mainloop()


