"""
Program: weatherTest.py
Author: yahoo/nerdyGinger
Serves as the webhook central for V1-O; functionality right now includes
getting weather forecasts, times for sunrise/sunset, and telling the
time.
"""

import urllib, urllib.request, json, datetime
import json, os, pytz
from flask import Flask, request, make_response

MONTHS = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "June",
          "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec" }

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
        res = weatherAction(req.get("result").get("contexts")[0].get("parameters").get("address"),
                            req.get("result").get("contexts")[0].get("parameters").get("date-time"))
    elif (req.get("result").get("action") == "sunrise"):
        res =  sunrise()
    elif (req.get("result").get("action") == "sunset"):
        res = sunset()
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

def weatherAction(city, date):
    try:
        splitDate = date.split("-")
        convDate = splitDate[2] + " " + MONTHS.get(splitDate[1]) + " " + splitDate[0]
    except:
        convDate = datetime.datetime.now().strftime("%d %b %Y")
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = ("select item from weather.forecast where woeid in " +
        "(select woeid from geo.places(1) where text='" + city + "')")
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    container = data['query']['results']
    sub = container.get("channel").get("item").get("forecast")
    forecast = "unknown"
    for i in sub:
        if (i.get("date") == convDate):
            text = ("The forecast in " + city + " on " + convDate + " is " + 
                    i.get("text") + " with a high of " + i.get("high") + ".")
    return { "speech": text,
             "displayText": text,
             "source": "yahooWeather" }

def sunrise():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select astronomy.sunrise from weather.forecast where woeid=12782768"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    container = data['query']['results']
    sub = container.get("channel").get("astronomy").get("sunrise")
    return { "speech": ("Sunrise today is at " + sub + "."),
             "displayText": ("Sunrise today is at " + sub + "."),
             "source": "yahooWeather" }

def sunset():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select astronomy.sunset from weather.forecast where woeid=12782768"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    container = data['query']['results']
    sub = container.get("channel").get("astronomy").get("sunset")
    return { "speech": ("Sunset today is at " + sub + "."),
             "displayText": ("Sunset today is at " + sub + "."),
             "source": "yahooWeather" }

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

def wakeup():
    return { "speech": "The server is already awake.",
             "displayText": "The server is already awake.",
             "source": "heroku" }

#-----------------------------------------------------------------------

def test():
    now = datetime.datetime.now(pytz.timezone("US/Central"))
    stringTime = now.strftime("%I:%M%p")
    print(stringTime)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    #test()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port = port, host='0.0.0.0')




    
