"""
Program: weatherActions.py
Author: nerdyGinger
Off-loads weather functions from the main webhook. Props to yahooWeatherAPI.
Contains:
basic weather, temperature, weather/outfit, sunrise, and sunset actions.
"""
import pytz, datetime, v1o_webhook, random
from constants import *

def weatherAction(city, date):
    #gets simple weather forecast data based on city and date
    convDate = v1o_webhook.convertDate(date)
    yql_query = ("select item from weather.forecast where woeid in " +
        "(select woeid from geo.places(1) where text='" + city + "')")
    container = v1o_webhook.yahooWeather(yql_query)
    sub = container.get("channel").get("item").get("forecast")
    forecast = "unknown"
    text = "Unable to find data."
    for i in sub:
        if (i.get("date") == convDate):
            randomText = random.choice(RANDOM_FORECAST)
            text = (randomText[0] + city + randomText[1] + convDate[:-5] +
                    randomText[2] + i.get("text") + randomText[3] +
                    i.get("high") + randomText[4])
    return { "speech": text,
             "displayText": text,
             "source": "yahooWeather" }

def weatherTemperature(city, temp, date):
    #returns temperature data given city, date, and optional temperature
    #qualification, i.e. warm, chilly, cold, etc. 
    try:
        tempRange = TEMPS.get(temp).split(";")
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
                    randomText = random.choice(RANDOM_TEMP_RANGE)
                    text = (randomText[0] + convDate[:-5] + randomText[1] +
                            str(high) + randomText[2] + temp + randomText[3])
                elif (high < int(tempRange[0])):
                    randomText = random.choice(RANDOM_TEMP_DIFF)
                    text = (randomText[0] + convDate[:-5] + randomText[1] +
                            sttr(high) + randomText[2] +
                            TEMPS_COOLER.get(temp) + randomText[3])
                else:
                    randomText = random.choice(RANDOM_TEMP_DIFF)
                    text = (randomText[0] + convDate[:-5] + randomText[1] +
                            str(high) + randomText[2] + TEMPS_WARMER.get(temp)
                            + randomText[3])
    except:
        convDate = v1o_webhook.convertDate(date)
        yql_query = ("select item from weather.forecast where woeid in " +
            "(select woeid from geo.places(1) where text='" + city + "')")
        container = v1o_webhook.yahooWeather(yql_query)
        sub = container.get("channel").get("item").get("forecast")
        forecast = "unknown"
        for i in sub:
            if (i.get("date") == convDate):
                randomText = random.choice(RANDOM_TEMP)
                text = (randomText[0] + convDate[:-5] + randomText[1] +
                        str(i.get("high")) + randomText[2])
    return { "speech": text,
         "displayText": text,
         "source": "yahooWeather" }

def weatherOutfit(city, date, outfit):
    #returns temperature/weather data given city, date, and outfit item
    convDate = v1o_webhook.convertDate(date)
    if outfit in OUTFIT_COLD:
        return weatherTemperature(city, "cold", date)
    elif (outfit in OUTFIT_CHILLY):
        return weatherTemperature(city, "chilly", date)
    elif outfit in OUTFIT_WARM:
        return weatherTemperature(city, "warm", date)
    elif (outfit in OUTFIT_CONDITIONS.keys()):
        conditions = CONDITIONS.get(
                     OUTFIT_CONDITIONS.get(outfit)).split(";")
        yql_query = ("select item from weather.forecast where woeid in " +
                     "(select woeid from geo.places(1) where text='" + city + "')")
        container = v1o_webhook.yahooWeather(yql_query)
        sub = container.get("channel").get("item").get("forecast")
        for i in sub:
            if (i.get("date") == convDate):
                for j in conditions:
                    if j in i.get("text").lower():
                        randomText = random.choice(RANDOM_OUTFITS_POSITIVE)
                        return { "speech": (randomText[0] + convDate[:-5] + randomText[1]
                                            + i.get("text") + randomText[2] + outfit +
                                            randomText[3]),
                                 "displayText": (randomText[0] + convDate[:-5] + randomText[1]
                                            + i.get("text") + randomText[2] + outfit +
                                            randomText[3]),
                                 "source": "yahooWeather" }
                randomText = random.choice(RANDOM_OUTFITS_NEGATIVE)
                return { "speech": (randomText[0] + convDate[:-5] + randomText[1] +
                                    i.get("text") + randomText[2]),
                         "displayText": (randomText[0] + convDate[:-5] + randomText[1] +
                                    i.get("text") + randomText[2]),
                         "source": "yahooWeather" }
    else:
        return weatherAction(city, date)

def sunrise():
    #returns time of sunrise on current date
    yql_query = "select astronomy.sunrise from weather.forecast where woeid=12782768"
    container = v1o_webhook.yahooWeather(yql_query)
    sub = container.get("channel").get("astronomy").get("sunrise")
    return { "speech": ("Sunrise today is at " + sub + "."),
             "displayText": ("Sunrise today is at " + sub + "."),
             "source": "yahooWeather" }

def sunset():
    #returns time of sunset on current date
    yql_query = "select astronomy.sunset from weather.forecast where woeid=12782768"
    container = v1o_webhook.yahooWeather(yql_query)
    sub = container.get("channel").get("astronomy").get("sunset")
    return { "speech": ("Sunset today is at " + sub + "."),
             "displayText": ("Sunset today is at " + sub + "."),
             "source": "yahooWeather" }
