"""
Program: constants.py
Author: nerdyGinger
Constant variables for v1o_webhook.py and branching files.
"""

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


