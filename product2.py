from twilio.rest import Client
#from server import *
import tkinter
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from PIL import Image, ImageTk

# The phone number is +12568575941
#import server.py

listOfTPnumbers = []
listOfHSnumbers = []
listOfFaceMaskNumbers = []
listOfNumbers = []

numOfTimesRan = 0
app = Flask(__name__)
#app.run(debug=True)

TPText = open("TPnumbers.txt", "w+")
HSText = open("HSnumbers.txt", "w+")
FMText = open("FMnumbers.txt", "w+")

previousBodyNumber = '0'

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    global previousBodyNumber
    global numOfTimesRan
    numOfTimesRan += 1
    print("incoming_sms() has ran this many times:" + str(numOfTimesRan))
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    number = request.values.get('From', None)

    # Start our TwiML response
    resp = MessagingResponse()

    if len(body) == 5:
        incoming_zip(body, previousBodyNumber)
        resp.message("Thank you for your zip code!")
        return str(resp)
    
    if body == '1': 
        if number not in listOfTPnumbers:
            listOfTPnumbers.append(number)
            TPText.write("%s\n" % number)
            resp.message("We will text you when toilet paper is available")
            resp.message("Please enter your ZIP Code so that local stores can update you")
            previousBodyNumber = 1
        else:
            resp.message("You are already subscribed to toilet paper notifications")
    elif body == '2':
        if number not in listOfHSnumbers:
            listOfHSnumbers.append(number)
            HSText.write("%s\n" % number)
            resp.message("We will text you when hand sanitizer is available")
            resp.message("Please enter your ZIP Code so that local stores can update you")
            previousBodyNumber = 2
        else:
            resp.message("You are already subscribed to hand sanitizer notifications")
    elif body == '3':
        if number not in listOfFaceMaskNumbers:
            listOfFaceMaskNumbers.append(number)
            FMText.write("%s\n" % number)
            resp.message("We will text you when face masks are available")
            resp.message("Please enter your ZIP Code so that local stores can update you")
            previousBodyNumber = 3
        else:
            resp.message("You are already subscribed to face mask notifications")
    else:
        resp.message("You are enrolled in Shopper Alert inventory service. To buy toilet paper, text 1. To buy hand saniter, text 2. To buy face masks, text 3")
    
    return str(resp)

def incoming_zip(number, body):
    zipCode = request.values.get('Body', None)
    print("zipCode in incoming-zip" + zipCode)
    print("body: " + str(body))
    if body == 1:
        TPText.write("%s\n" % zipCode)
        return True
    if body == 2:
        print("Its in body=2")
        HSText.write("%s\n" % zipCode)
        return True
    if body == 3:
        FMText.write("%s\n" % zipCode)
        return True
    return False
    

if __name__ == "__main__":
    app.run(debug=True)
#global string var
itemString = "Toilet Paper"

TPText.close()
FMText.close()
HSText.close()

#grabs input from the first Entry (item) (This might be useless now)
# def retrieve_input():
#     print("Input: %s\n" % (e1.get()))
#     return str(e1.get())

#grabs input from the second Entry (quantity)    
def retrieve_quantity():
    return str(e2.get())
# def retrieve_item():
#     return str(eL.get())
def retrieve_store():
    return str(sL.get())
def retrieve_zip():
    return int(zL.get())
    
#start twilio

# Your Account SID from twilio.com/console
account_sid = "ACaef97a4585c34bfb073716c0bfbc52db"
# Your Auth Token from twilio.com/console
auth_token = "xxxx"

client = Client(account_sid, auth_token)

def sendMessage():
    TPTell = open("TPnumbers.txt", "r+")
    HSTell = open("HSnumbers.txt", "r+")
    FMTell = open("FMnumbers.txt", "r+")
    print("got to sendMessage")
    #this var will hold the complteted string
    string = "The item " + itemString + " is now in stock in " + retrieve_store() + " at the ZIP Code: " + str(retrieve_zip()) + "." + " There are " + retrieve_quantity() + " available."
    #this line actually sends the message


    if itemString == "Toilet Paper": 
        with TPTell as filehandle:
            line = filehandle.readlines()
            lineIndex = 0
            while lineIndex < len(line):
                phoneNumberOnly = line[lineIndex]
                print("new phone num")
                print(phoneNumberOnly)
                zipCodeOnly = line[lineIndex + 1]
                print(zipCodeOnly)
                lineIndex += 2
                print("For testing: phone number = " + phoneNumberOnly[0:12] + " zip code only =" + zipCodeOnly)
                print("retrieve_zip output=" + str(retrieve_zip()))
                print("zipCodeOnly=" + zipCodeOnly)
                result = int(zipCodeOnly) - int(retrieve_zip())
                print("result =" + str(result))
                #print(int(zipCodeOnly) == retrieve_zip())
                if (result == 0):
                    print("about to send message to " + phoneNumberOnly[0:12])
                    message = client.messages.create(to=phoneNumberOnly[0:12], from_="+12568575941", body=string)
        TPTell.close()
    if itemString == "Hand Sanitizer":
        with HSTell as filehandle:
            line = filehandle.readlines()
            lineIndex = 0
            while lineIndex < len(line):
                phoneNumberOnly = line[lineIndex]
                zipCodeOnly = line[lineIndex + 1]
                lineIndex += 2
                result = int(zipCodeOnly) - int(retrieve_zip())
                if (result == 0):
                    message = client.messages.create(to=phoneNumberOnly[0:12], from_="+12568575941", body=string)
        HSTell.close()
    if itemString == "Face Mask":
        with FMTell as filehandle:
            line = filehandle.readlines()
            lineIndex = 0
            while lineIndex < len(line):
                phoneNumberOnly = line[lineIndex]
                zipCodeOnly = line[lineIndex + 1]
                lineIndex += 2
                result = int(zipCodeOnly) - int(retrieve_zip())
                if (result == 0):
                    message = client.messages.create(to=phoneNumberOnly[0:12], from_="+12568575941", body=string)
        FMTell.close()

#start GUI
#retrieve input from the text boxes:


m=tkinter.Tk() #m is the name of the main window object
m.geometry('1100x910')
#image1 = tkinter.Image(file = "toiletpaper.jpg")
photo = Image.open("coronacomp.png")
image1 = ImageTk.PhotoImage(photo)
label_for_image = tkinter.Label(m, image=image1)
label_for_image.pack()
m.title("Shopper Alert")

storeLabel = tkinter.Label(m, text="Enter your store here")
storeLabel.pack()

sL = tkinter.Entry(m)
sL.pack()

zipCodeLabel = tkinter.Label(m, text="Enter your ZIP code here")
zipCodeLabel.pack()

zL = tkinter.Entry(m)
zL.pack()


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
toiletPaperButton.select()

def handSantizerClick():
    print("santizer ran")
    global itemString
    itemString = "Hand Sanitizer"
    print(itemString)

    
handSanitizerButton = tkinter.Radiobutton(m, text = "Hand Sanitizer", value = 0, command = handSantizerClick)
handSanitizerButton.pack()
handSanitizerButton.deselect()


def faceMaskClick():
    print("face mask ran")
    global itemString
    itemString = "Face Mask"
    print(itemString)

faceMaskButton = tkinter.Radiobutton(m, text = "Face Mask", value=2, command=faceMaskClick)
faceMaskButton.pack()
faceMaskButton.deselect()

label2 = tkinter.Label(m, text="Input quantity of item here")
label2.pack()
#e2 contains the quantity of the item
e2 = tkinter.Entry(m)
e2.pack()

getButton = tkinter.Button(m, text="send message entered", width=25, command=sendMessage)
getButton.pack()

button = tkinter.Button(m, text="close window", width=25, command=m.destroy, bg="#ff0000", fg = "#ff0000")
button.pack()

m.mainloop()


