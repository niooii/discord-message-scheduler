import datetime
import sys
import tkinter
import threading
from tkinter import messagebox
import requests
import time
import logging
from datetime import datetime

global msg
global auth
global chnl

global inc

consoleIndex = 0



def getTimeStampedString(string):
    timestamp = datetime.now().timestamp()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%m-%d-%Y %H:%M:%S")
    return '[' + str_date_time + ']  ' + string


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def sendmsgInitial(msg, auth, chnl, delaytime, initial):
    payload = {
        'content': f'{msg}'
    }

    header = {
        'authorization': f'{auth}'
    }
    r = requests.post(f"https://discord.com//api/v9/channels/{chnl}/messages", data=payload, headers=header)

    if int(r.status_code / 100) == 2:
        if not initial:
            consoleLog("Message successfully sent!")
        return True
    else:
        if not initial:
            consoleLog("Error sending message...")
        return False


def sendmsgLoop(msg, auth, chnl, delaytime):
    consoleLog("Thread created!")
    while True:
        time.sleep(delaytime)

        sendmsgInitial(msg, auth, chnl, delaytime, False)


def consoleLog(string):
    global consoleIndex
    consoleIndex += 1
    console.insert(consoleIndex, getTimeStampedString(string))
    console.yview(consoleIndex)


def start():
    strIn = msgEntry.get(1.0, 'end-1c')
    authToken = authTokenEntry.get()
    channelId = channelEntry.get()
    delayTime = delayEntry.get()

    if len(strIn) > 0:

        if sendmsgInitial(strIn, authToken, channelId, delayTime, True):

            consoleLog("Test message successfully sent!")
            consoleLog("Creating thread...")
            t = threading.Thread(target=sendmsgLoop, args=(strIn, authToken, channelId, float(delayTime)))
            t.daemon = True
            t.start()
        else:
            consoleLog("Failed to send message; Thread will not be created.")
    else:
        consoleLog("Cannot send empty message..")


window = tkinter.Tk()


def on_closing():
    if messagebox.askokcancel("Are you sure?", "Closing this window will end all threads. Proceed?"):
        window.destroy()
        sys.exit(0)

inc = False

window.protocol("WM_DELETE_WINDOW", on_closing)

window.title("Discord Message Scheduler")
frame = tkinter.Frame(window)
frame.pack()

inputFrame = tkinter.LabelFrame(frame, text="Information")
inputFrame.grid(row=0, column=0, padx=20, pady=20)

authTokenLabel = tkinter.Label(inputFrame, text="Auth Token")
authTokenLabel.grid(row=0, column=0)

authTokenEntry = tkinter.Entry(inputFrame)
authTokenEntry.grid(row=1, column=0, sticky="news")

channelLabel = tkinter.Label(inputFrame, text="Channel ID")
channelLabel.grid(row=2, column=0)

channelEntry = tkinter.Entry(inputFrame)
channelEntry.grid(row=3, column=0, sticky="news")

delayLabel = tkinter.Label(inputFrame, text="Time between messages (in seconds)")
delayLabel.grid(row=4, column=0)

delayEntry = tkinter.Entry(inputFrame)
delayEntry.grid(row=5, column=0)

msgLabel = tkinter.Label(inputFrame, text="Message")
msgLabel.grid(row=6, column=0)

msgEntry = tkinter.Text(inputFrame)
msgEntry.grid(row=7, column=0)

consoleFrame = tkinter.LabelFrame(frame, text="Console")
consoleFrame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

console = tkinter.Listbox(consoleFrame)
console.pack(fill="both", expand=True)

button = tkinter.Button(frame, text="Start Loop", command=start)
button.grid(row=2, column=0, sticky="news", padx=20, pady=10)

checkbox = tkinter.Checkbutton(frame, text="Increment number", command=(lambda : not ))

for widget in inputFrame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

window.mainloop()
