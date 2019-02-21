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
    container = v1o_webhook.yahooWeather(
                            {'location': city, 'format': 'json'})
    sub = container.get("forecasts")
    forecast = "unknown"
    text = "Unable to find data."
    for i in sub:
        if (i.get("date") == convDate):
            randomText = random.choice(RANDOM_FORECAST)
            text = (randomText[0] + city + randomText[1] + convDate[:-5] +
                    randomText[2] + i.get("text") + randomText[3] +
                    i.get("high") + randomText[4])
    return { "fulfillmentText": text,
             "source": "yahooWeather" }

def weatherTemperature(city, temp, date):
    #returns temperature data given city, date, and optional temperature
    #qualification, i.e. warm, chilly, cold, etc. 
    try:
        tempRange = TEMPS.get(temp).split(";")
        convDate = v1o_webhook.convertDate(date)
        container = v1o_webhook.yahooWeather(
                                {'location': city, 'format': 'json'})
        sub = container.get("forecasts")
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
        container = v1o_webhook.yahooWeather(
                                {'location': city, 'format': 'json'})
        sub = container.get("channel").get("item").get("forecast")
        forecast = "unknown"
        for i in sub:
            if (i.get("date") == convDate):
                randomText = random.choice(RANDOM_TEMP)
                text = (randomText[0] + convDate[:-5] + randomText[1] +
                        str(i.get("high")) + randomText[2])
    return { "fulfillmentText": text,
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
        container = v1o_webhook.yahooWeather(
                                {'location': city, 'format': 'json'})
        sub = container.get("forecasts")
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
    container = v1o_webhook.yahooWeather(
                            {'location': 'sioux falls,sd', 'format': 'json'})
    sub = container.get("current_observation").get("astronomy").get("sunrise")
    return { "fulfillmentText": ("Sunrise today is at " + sub + "."),
             "source": "yahooWeather" }

def sunset():
    #returns time of sunset on current date
    container = v1o_webhook.yahooWeather(
                            {'location': 'sioux falls,sd', 'format': 'json'})
    sub = container.get("current_observation").get("astronomy").get("sunset")
    return { "fulfillmentText": ("Sunset today is at " + sub + "."),
             "source": "yahooWeather" }
