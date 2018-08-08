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

#--------------------------------------------------------------------
#--- Global variables ---

BASE_URL = "https://query.yahooapis.com/v1/public/yql?"

MONTHS = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "June",
          "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec" }

TEMPS = {"freezing": "-100;10", "cold": "11;32", "chilly": "33;55", "warm": "55;75",
         "hot": "76;200" }

TEMPS_COOLER = { "cold": "freezing", "chilly": "cold", "warm": "chilly", "hot": "warm" }

TEMPS_WARMER = { "freezing": "cold", "cold": "chilly", "chilly": "warm", "warm": "hot" }

OUTFIT_COLD = [ "jacket", "hat", "turtleneck", "coat", "scarf", "pants", "gloves" ]

OUTFIT_CHILLY = [ "sweatshirt", "hoodie", "cardigan", "long sleeves", "shawls", "jeans" ]

OUTFIT_WARM = [ "t-shirt", "shorts", "tank top", "sandals", "bathing suit", "swim suit",
                "skirt", "capri", "flip flops" ]

OUTFIT_CONDITIONS = { "umbrella": "rain", "rain jacket": "rain", "rain coat": "rain",
                       "boots": "snow", "ski pants": "snow", "snow pants": "snow",
                       "sunglasses": "sun", "sunscreen": "sun" }

CONDITIONS = { "severe": "tornado;tropical storm;hurricane;severe;hail;blizzard",
               "snow": "snow",
               "rain": "thunderstorm;rain;sleet;drizzle;shower",
               "windy": "windy;blustery",
               "visibility": "foggy;haze;smokey;dust",
               "sun": "hot;sunny;fair;partly cloudy"}

OUTFITS_TEMPS = { }
            
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
        res = weatherAction(
            req.get("result").get("contexts")[0].get("parameters").get("address"),
            req.get("result").get("contexts")[0].get("parameters").get("date-time"))
    elif (req.get("result").get("action") == "weatherTemperature"):
        res = weatherTemperature(
            req.get("result").get("contexts")[0].get("parameters").get("address"),
            req.get("result").get("contexts")[0].get("parameters").get("temperature"),
            req.get("result").get("contexts")[0].get("parameters").get("date-time"))
    elif (req.get("result").get("action") == "weatherOutfit"):
        res = weatherOutfit(
            req.get("result").get("contexts")[0].get("parameters").get("address"),
            req.get("result").get("contexts")[0].get("parameters").get("date-time"),
            req.get("result").get("contexts")[0].get("parameters").get("outfit"))
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
#--- Webhook actions ---

def weatherAction(city, date):
    convDate = convertDate(date)
    yql_query = ("select item from weather.forecast where woeid in " +
        "(select woeid from geo.places(1) where text='" + city + "')")
    container = yahooWeather(yql_query)
    sub = container.get("channel").get("item").get("forecast")
    forecast = "unknown"
    for i in sub:
        if (i.get("date") == convDate):
            text = ("The forecast in " + city + " on " + convDate[:-4] + " is " + 
                    i.get("text") + " with a high of " + i.get("high") + ".")
    return { "speech": text,
             "displayText": text,
             "source": "yahooWeather" }

def weatherTemperature(city, temp, date):
    try:
        tempRange = TEMPS.get(temp).split(";")
        convDate = convertDate(date)
        yql_query = ("select item from weather.forecast where woeid in " +
            "(select woeid from geo.places(1) where text='" + city + "')")
        container = yahooWeather(yql_query)
        sub = container.get("channel").get("item").get("forecast")
        forecast = "unknown"
        for i in sub:
            if (i.get("date") == convDate):
                high = int(i.get("high"))
                if (high >= int(tempRange[0]) and high <= int(tempRange[1])):
                    text = ("The high on " + convDate[:-4] + " is supposed to be " +
                            str(high) + " degrees, so it should be " + temp + ".")
                elif (high < int(tempRange[0])):
                    text = ("The high on " + convDate[:-4] + " is supposed to be " +
                            sttr(high) + " degrees, so it may be rather " +
                            TEMPS_COOLER.get(temp) + ".")
                else:
                    text = ("The high on " + convDate[:-4] + " is supposed to be " +
                            str(high) + " degrees, so it may be rather " +
                            TEMPS_WARMER.get(temp) + ".")
    except:
        convDate = convertDate(date)
        yql_query = ("select item from weather.forecast where woeid in " +
            "(select woeid from geo.places(1) where text='" + city + "')")
        container = yahooWeather(yql_query)
        sub = container.get("channel").get("item").get("forecast")
        forecast = "unknown"
        for i in sub:
            if (i.get("date") == convDate):
                text = ("The high on " + convDate[:-4] + " is supposed to be " +
                        str(i.get("high")) + " degrees.")
    return { "speech": text,
         "displayText": text,
         "source": "yahooWeather" }

def weatherOutfit(city, date, outfit):
    convDate = convertDate(date)
    if outfit in OUTFIT_COLD:
        return weatherTemperature(city, "cold", date)
    elif (outfit in OUTFIT_CHILLY):
        return weatherTemperature(city, "chilly", date)
    elif outfit in OUTFIT_WARM:
        return weatherTemperature(city, "warm", date)
    elif (outfit in OUTFIT_CONDITIONS.keys()):
        conditions = CONDITIONS.get(OUTFIT_CONDITIONS.get(outfit)).split(";")
        yql_query = ("select item from weather.forecast where woeid in " +
                     "(select woeid from geo.places(1) where text='" + city + "')")
        container = yahooWeather(yql_query)
        sub = container.get("channel").get("item").get("forecast")
        for i in sub:
            if (i.get("date") == convDate):
                for j in conditions:
                    if j in i.get("text").lower():
                        return { "speech": ("Yes, the forecast for " + convDate[:-4] + " is "
                                            + i.get("text") + ", so your " + outfit +
                                            " may be a wise choice."),
                                 "displayText": ("Yes, the forecast for " + convDate[:-4] +
                                                 " is " + i.get("text") + ", so your " +
                                                 outfit + " may be a wise choice."),
                                 "source": "yahooWeather" }
                return { "speech": ("The forecast for " + convDate[:-4] + " is actually " +
                                    i.get("text") + "."),
                         "displayText": ("The forecast for " + convDate[:-4] + " is actually " +
                                    i.get("text") + "."),
                         "source": "yahooWeather" }
    else:
        return weatherAction(city, date)
        
        
    return { "speech": "This functionality is still in development. My apologies.",
             "displayText": "This functionality is still in development. My apologies.",
             "source": "yahooWeather" }


def sunrise():
    yql_query = "select astronomy.sunrise from weather.forecast where woeid=12782768"
    container = yahooWeather(yql_query)
    sub = container.get("channel").get("astronomy").get("sunrise")
    return { "speech": ("Sunrise today is at " + sub + "."),
             "displayText": ("Sunrise today is at " + sub + "."),
             "source": "yahooWeather" }

def sunset():
    yql_query = "select astronomy.sunset from weather.forecast where woeid=12782768"
    container = yahooWeather(yql_query)
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
    print(weatherOutfit("Sioux Falls", "2018-08-09", "hat"))

#-----------------------------------------------------------------------
#--- Run main ---

if __name__ == '__main__':
    #test()
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port = port, host='0.0.0.0')




    
