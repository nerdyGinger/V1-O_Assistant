"""
Program: weatherActions.py
Author: nerdyGinger
Off-loads weather functions from the main webhook.
Contains:
basic weather, temperature, weather/outfit, sunrise, and sunset actions.
"""
import pytz, datetime, v1o_webhook 

def weatherAction(city, date):
    convDate = v1o_webhook.convertDate(date)
    yql_query = ("select item from weather.forecast where woeid in " +
        "(select woeid from geo.places(1) where text='" + city + "')")
    container = v1o_webhook.yahooWeather(yql_query)
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
        tempRange = v1o_webhook.TEMPS.get(temp).split(";")
        convDate = v1o_webhook.convertDate(date)
        yql_query = ("select item from weather.forecast where woeid in " +
            "(select woeid from geo.places(1) where text='" + city + "')")
        container = v1o_webhook.yahooWeather(yql_query)
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
        convDate = v1o_webhook.convertDate(date)
        yql_query = ("select item from weather.forecast where woeid in " +
            "(select woeid from geo.places(1) where text='" + city + "')")
        container = v1o_webhook.yahooWeather(yql_query)
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
    convDate = v1o_webhook.convertDate(date)
    if outfit in v1o_webhook.OUTFIT_COLD:
        return weatherTemperature(city, "cold", date)
    elif (outfit in v1o_webhook.OUTFIT_CHILLY):
        return weatherTemperature(city, "chilly", date)
    elif outfit in v1o_webhook.OUTFIT_WARM:
        return weatherTemperature(city, "warm", date)
    elif (outfit in v1o_webhook.OUTFIT_CONDITIONS.keys()):
        conditions = v1o_webhook.CONDITIONS.get(
                     v10_webhook.OUTFIT_CONDITIONS.get(outfit)).split(";")
        yql_query = ("select item from weather.forecast where woeid in " +
                     "(select woeid from geo.places(1) where text='" + city + "')")
        container = v1o_webhook.yahooWeather(yql_query)
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
    container = v1o_webhook.yahooWeather(yql_query)
    sub = container.get("channel").get("astronomy").get("sunrise")
    return { "speech": ("Sunrise today is at " + sub + "."),
             "displayText": ("Sunrise today is at " + sub + "."),
             "source": "yahooWeather" }

def sunset():
    yql_query = "select astronomy.sunset from weather.forecast where woeid=12782768"
    container = v1o_webhook.yahooWeather(yql_query)
    sub = container.get("channel").get("astronomy").get("sunset")
    return { "speech": ("Sunset today is at " + sub + "."),
             "displayText": ("Sunset today is at " + sub + "."),
             "source": "yahooWeather" }
