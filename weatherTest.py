"""
Program: weatherTest.py
Author: yahoo/Morgan
Gets current weather data for Sioux Falls and prints time/temp/condition.
"""

import urllib, urllib.request, json, datetime
import json, os
from flask import Flask, request, make_response

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
        res = weatherAction()
    elif (req.get("result").get("action") == "time.get"):
        current = datetime.datetime.now().strftime("%I:%M%p")
        res = current
    else:
        return {}
    print("Result: " + res)
    return res

def weatherAction():
    print("Weather action called.")
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select item.condition from weather.forecast where woeid=12782768"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    container = data['query']['results']
    sub = container.get("channel").get("item").get("condition")
    text = ("The weather in Sioux Falls is " + sub.get("temp") +
        " degrees and " + sub.get("text").lower() + ".")
    return { "speech": text, "displayText": text, "source": "yahooWeather" }

#-----------------------------------------------------------------------
def test():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select item.condition from weather.forecast where woeid=12782768"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    container = data['query']['results']
    sub = container.get("channel").get("item").get("condition")
    print ("Weather in Sioux Falls at "  +
           datetime.datetime.now().strftime("%I:%M%p") + " is " + 
           sub.get("temp") + " degrees and " + sub.get("text").lower() + ".")
    input()

#-----------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port = port, host='0.0.0.0')




    
