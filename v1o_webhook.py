"""
Program: v1o_webhook.py
Author: nerdyGinger
Serves as the webhook central for V1-O; functionality right now includes
getting weather forecasts, times for sunrise/sunset, telling the time, and
doing very simple web searches. Contains functions to pass parameters on to
platform application for timer, alarm, and reminders. Uses yahooWeatherApi
and duckduckgoApi.
"""

import urllib, urllib.request, json, datetime, random, requests, requests.auth
import json, os, pytz, weatherActions, duckduckpy, requests, threading
import uuid, time, hmac, hashlib
from flask import Flask, request, make_response
from base64 import b64encode
from constants import *


#--------------------------------------------------------------------------
#--- Connction functions ---

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    #hooking up to V1-O
    print("Received hook...")
    req = request.get_json(silent=True, force=True)
    result = processRequest(req)
    print("Request: " + json.dumps(req, indent=4))
    result = json.dumps(result, indent=4)
    r = make_response(result)
    r.headers['content-Type'] = "application/json"
    print("Returning...")
    return r

def processRequest(req):
    #sort out the requests/actions
    action = req.get("result").get("action")
    parameters = req.get("result").get("parameters")
    contextParameters = req.get("result").get("contexts")[0].get("parameters")
    if (action == "yahooWeatherForcast"):
        res = weatherActions.weatherAction(
            contextParameters.get("address"),
            contextParameters.get("date-time"))
    elif (action == "weatherTemperature"):
        res = weatherActions.weatherTemperature(
            contextParameters.get("address"),
            contextParameters.get("temperature"),
            contextParameters.get("date-time"))
    elif (action == "weatherOutfit"):
        res = weatherActions.weatherOutfit(
            contextParameters.get("address"),
            contextParameters.get("date-time"),
            contextParameters.get("outfit"))
    elif (action == "setTimer"):
        res = timer(parameters.get("duration").get("amount"),
                    parameters.get("duration").get("unit"))
    elif (action == "reminders.add"):
        res = reminderAdd(parameters.get("date-time"),
                          parameters.get("name"))
    elif (action == "alarm.set"):
        res = alarmSet(parameters.get("alarm-name"),
                       parameters.get("time"),
                       parameters.get("date"),
                       parameters.get("recurrence"))
    elif (action == "alarm.remove"):
        res = alarmRemove(parameters.get("time"),
                          parameters.get("date"),
                          parameters.get("all"))
    elif (action == "web.search"):
        res = search(contextParameters.get("q"))
    elif (action == "sunrise"):
        res =  weatherActions.sunrise()
    elif (action == "sunset"):
        res = weatherActions.sunset()
    elif (action == "time.get"):
        res = getTimeAction()
    elif (action == "wakeup"):
        res = wakeup()
    else:
        return { "speech": ("This request is unknown to me. I have logged this " +
                            "interaction for further development."),
                 "displayText": ("This request is unknown to me. I have logged this" +
                                 " interaction for further development."),
                 "source": "unknownCommand" }
    return res

#--------------------------------------------------------------
#--- Webhook actions ---

def getTimeAction():
    #returns current time in central US timezone
    now = datetime.datetime.now(pytz.timezone("US/Central"))
    stringTime = now.strftime("%I:%M%p")
    return ({ "speech": ("It is " + stringTime + "."),
                "displayText": ("It is " + stringTime + "."),
                "source": "pytime" })

def timer(amount, unit):
    #set timer -->under construction
    return { "speech": "Timer set.",
             "displayText": "Timer set.",
             "source": ("android;timer;" + str(amount) + ";" + unit) }

def search(query):
    #run wearch query via duckduckgo API
    response = duckduckpy.query(query, False, 'dict', False, 'duckduckpy 0.2',
                     True, True, False)
    result = "No results found."
    if(response["related_topics"] != []):
        result = (response["related_topics"][0]["text"])
    if(response["abstract"] != ""):
        result = (response["abstract"])
    randomText = random.choice(RANDOM_WEBSEARCH)
    return { "speech": randomText[0] + query + ": " + result,
             "displayText": randomText[0] + query + ": " + result,
             "source": "webSearch" }

def reminderAdd(datetime, reminder):
    #add reminder -->under construction
    randomText = random.choice(RANDOM_REMINDER_SET)
    return { "speech": randomText[0] + datetime + randomText[1],
             "displayText": randomText[0] + datetime + randomText[1],
             "source": "android;addReminder;" + str(datetime) + ";" + reminder }

def alarmSet(name, time, date, recurrence):
    #set alarm -->under construction
    return { "speech": "Unable to set alarm.",
             "displayText": "Unable to set alarm.",
             "source": "android;setAlarm;" + name + ";" + time + ";"
                                           + date + ";" + recurrence }

def alarmRemove(time, date, removeAll):
    #remove alarm -->under construction
    return { "speech": "Unable to remove alarm.",
             "displayText": "Unable to remove alarm.",
             "source": "android;removeAlarm;" + time + ";" + date + ";" + removeAll }

def wakeup():
    #should always return this if webhook is functioning properly
    return { "speech": "The server is already awake.",
             "displayText": "The server is already awake.",
             "source": "heroku" }



#-----------------------------------------------------------------------
#--- Helper functions ---

def convertDate(agentDate):
    #converts date from agent to yahoo-friendly format
    try:
        splitDate = agentDate.split("-")
        convDate = splitDate[2] + " " + MONTHS.get(splitDate[1]) + " " + splitDate[0]
    except:
        now = datetime.datetime.now(pytz.timezone("US/Central"))
        convDate = now.strftime("%d %b %Y")
    return convDate

def pingDyno():
    #pings dyno server every 30 minutes
    while True:
        requests.get("https://v1o-guts.herokuapp.com")
        print("*ping*")
        time.sleep(1800)

#-----------------------------------------------------------------------
#--- Test function ---

def test():
    print("we all good")

#-----------------------------------------------------------------------
#--- Run main ---

if __name__ == '__main__':
    #test()
    #"""
    port = int(os.getenv('PORT', 5000))
    pingThread = threading.Thread(target=pingDyno)
    pingThread.start()
    app.run(debug=False, port = port, host='0.0.0.0')
    #"""



    
