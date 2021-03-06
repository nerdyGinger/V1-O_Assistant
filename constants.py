"""
Program: constants.py
Author: nerdyGinger
Constant variables for v1o_webhook.py and branching files.
(Secret YahooApi values are in separate file for local dev,
and looked down tight for deployment)
"""

#-------------------------------------------------------------------------------
# --- URLs ---

DATABASE_URL = 'postgres://axlyomrdaqaswv:e11d7639f2225c11a0da95e26f7259ca219e3a40fa47fb76bddf031204dda2d1@ec2-54-243-128-95.compute-1.amazonaws.com:5432/d8b9hl8vmdved7'

BASE_URL = "https://weather-ydn-yql.media.yahoo.com/forecastrss?"

#-------------------------------------------------------------------------------
# --- Weather ---

MONTHS = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "June",
          "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec" }

TEMPS = {"freezing": "-100;10", "cold": "11;32", "chilly": "33;55", "warm": "55;75",
         "hot": "76;200" }

TEMPS_COOLER = { "cold": "freezing", "chilly": "cold", "warm": "chilly", "hot": "warm" }

TEMPS_WARMER = { "freezing": "cold", "cold": "chilly", "chilly": "warm", "warm": "hot" }

OUTFIT_COLD = [ "jacket", "hat", "turtleneck", "coat", "scarf", "pants", "gloves" ]

OUTFIT_CHILLY = [ "sweatshirt", "hoodie", "cardigan", "long sleeves", "shawl", "jeans" ]

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

#-------------------------------------------------------------------------------
# --- Randomizers ---

RANDOM_OUTFITS_POSITIVE = [ ["Yes, the forecast for ", " is ", ", so your ",
                             " may be a wise choice."],
                            ["The forecast for ", " is ", ", so your ",
                             " is a logical choice."],
                            ["On ", " the forecast is ", ". Your ",
                             " should work well."] ]
    
RANDOM_OUTFITS_NEGATIVE = [ ["Actually, the forecast for ", " is ", "."],
                            ["Well, you should know that the forecast on ",
                            " is ", "."],
                            ["I will leave the matter up to you. But the " +
                            "forecast for ", " is ", "."],
                            ["The forecast on ", " is actually ", "."],
                            ["You should not need it. The forecast for ", 
                             " is ", "."] ]

RANDOM_FORECAST = [ ["The weather in ", " on ", " is supposed to be ",
                     " with a high of ", "." ],
                    ["The forecast for ", " on ", " is ", " with a high of ",
                     "."],
                    ["In ", " on ", ", the weather should be ", " with " +
                     "a high of ", "."] ]

RANDOM_TEMP_DIFF = [ ["The high on ", " is supposed to be ", " degrees, so it " +
                       "may be rather ", "."],
                      ["On ", " it should be ", ", so it might be rather ", "."],
                      ["The temperature on ", " should be approximately ",
                       " degrees, so you it may feel ", "."] ]

RANDOM_TEMP_RANGE = [ ["The high on ", " is supposed to be " , " degrees, so it " +
                 "should be ", "."],
                ["On ", " it should be ", ", so ", " would be an appropriate" +
                 " description."],
                ["The temperature on ", " is predicted to be ", " degrees, so ",
                 " should describe the conditions accurately."] ]

RANDOM_TEMP = [ ["The high on ", " is supposed to be ", " degrees."],
                ["On ", " the high is ", " degrees."],
                ["The temperature on ", " should be around ", " degrees."],
                ["On ", " the high is expected to be ", "."],
                ["The high on ", " should be ", "."],
                ["The temperature on ", " is predicted to be ", "."] ]

RANDOM_REMINDER_SET = [ ["I will remind you at ", "."],
                        ["Reminder set for ", "."],
                        ["Okay, I will remind you at ", "."],
                        ["Okay, your reminder is set for ", "."],
                        ["Okay, at ", " I will activate your reminder."],
                        ["Your reminder is set for ", "."] ]

RANDOM_WEBSEARCH = [ ["Web result for ", ": "],
                     ["Here is what I found for ", ": "],
                     ["This is the web result for ", ": "],
                     ["Search result for ", ": "] ]
                



