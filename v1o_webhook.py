"""
Program: v1o_webhook.py
Author: yahoo/nerdyGinger
Serves as the webhook central for V1-O; functionality right now includes
getting weather forecasts, times for sunrise/sunset, and telling the
time.
"""

import urllib, urllib.request, json, datetime
import json, os, pytz, weatherActions
from flask import Flask, request, make_response
from constants import *

#--------------------------------------------------------------------------
#--- Connction functions ---

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
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
    if (req.get("result").get("action") == "yahooWeatherForcast"):
        res = weatherActions.weatherAction(
            req.get("result").get("contexts")[0].get("parameters").get("address"),
            req.get("result").get("contexts")[0].get("parameters").get("date-time"))
    elif (req.get("result").get("action") == "weatherTemperature"):
        res = weatherActions.weatherTemperature(
            req.get("result").get("contexts")[0].get("parameters").get("address"),
            req.get("result").get("contexts")[0].get("parameters").get("temperature"),
            req.get("result").get("contexts")[0].get("parameters").get("date-time"))
    elif (req.get("result").get("action") == "weatherOutfit"):
        res = weatherActions.weatherOutfit(
            req.get("result").get("contexts")[0].get("parameters").get("address"),
            req.get("result").get("contexts")[0].get("parameters").get("date-time"),
            req.get("result").get("contexts")[0].get("parameters").get("outfit"))
    elif (req.get("result").get("action") == "sunrise"):
        res =  weatherActions.sunrise()
    elif (req.get("result").get("action") == "sunset"):
        res = weatherActions.sunset()
    elif (req.get("result").get("action") == "web.search"):
        res = search(req.get("result").get("parameters").get("q"))
    elif (req.get("result").get("action") == "time.get"):
        res = getTimeAction()
    elif (req.get("result").get("action") == "setTimer"):
        res = timer(req.get("result").get("parameters").get("duration").get("amount"),
                    req.get("result").get("parameters").get("duration").get("unit"))
    elif (req.get("result").get("action") == "wakeup"):
        res = wakeup()
    else:
        return {}
    return res

#--------------------------------------------------------------
#--- Webhook actions ---

def getTimeAction():
    now = datetime.datetime.now(pytz.timezone("US/Central"))
    stringTime = now.strftime("%I:%M%p")
    return ({ "speech": ("It is " + stringTime + "."),
                "displayText": ("It is " + stringTime + "."),
                "source": "pytime" })

def timer(amount, unit):
    return { "speech": "Timer set.",
             "displayText": "Timer set.",
             "source": ("android;" + str(amount) + ";" + unit) }

def search(query):
    return { "speech": "Unable to search the web for " + query + ".",
             "displayText": "Unable to search the web for " + query + ".",
             "source": "webSearch" }

def wakeup():
    return { "speech": "The server is already awake.",
             "displayText": "The server is already awake.",
             "source": "heroku" }



#-----------------------------------------------------------------------
#--- Helper functions ---

def yahooWeather(query):
    yql_url = BASE_URL + urllib.parse.urlencode({'q':query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    return data['query']['results']

def convertDate(agentDate):
    try:
        splitDate = agentDate.split("-")
        convDate = splitDate[2] + " " + MONTHS.get(splitDate[1]) + " " + splitDate[0]
    except:
        now = datetime.datetime.now(pytz.timezone("US/Central"))
        convDate = now.strftime("%d %b %Y")
    return convDate

#-----------------------------------------------------------------------
#--- Test function ---

def test():
    print(weatherActions.weatherOutfit("Sioux Falls", "2018-08-09", "sunscreen"))

#-----------------------------------------------------------------------
#--- Run main ---

if __name__ == '__main__':
    #test()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port = port, host='0.0.0.0')




    
