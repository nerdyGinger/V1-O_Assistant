"""
Program: recipeDatabase.py
Author: nerdyGinger
Connection to Heroku database for updating and querying recipes.

vvv Initialized table/recipes vvv

cursor.execute('''CREATE TABLE recipies
                (id SERIAL PRIMARY KEY NOT NULL,
                name             TEXT  NOT NULL,
                description      TEXT          ,
                preptime         TEXT  NOT NULL,
                yield            TEXT  NOT NULL,
                ingredients    TEXT[]  NOT NULL,
                directions     TEXT[]  NOT NULL);''')

cursor.execute('''INSERT INTO recipies (name, description, preptime, yield, ingredients, directions)
                    VALUES
                            ( 'PB and J',
                            'A simple peanut butter and jelly sandwich.',
                            '5 min',
                            '1 sandwich',
                            ARRAY ['2 slices bread",
                                    "2 tbs peanut butter",
                                    "1 tbs jelly'],
                            ARRAY ['Spread the peanut butter on one slice of bread.',
                                    'Spread jelly on top of the peanut butter.',
                                    'Place other slice of bread on top.',
                                    'Enjoy!']
                            );''')
"""

import os, psycopg2, urllib.parse
#from secrets import *

def recipeQuery(recipeName):
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    recipe = "['No recipe found']"

    try:
        cursor = connection.cursor()
        cursor.execute('''SELECT name, description, preptime, yield, ingredients, directions FROM recipies
                          WHERE LOWER(name) = LOWER(%s);''', (recipeName,))
        recipe = (cursor.fetchall())
    except:
        print("Issue querying database!")
    finally:
        connection.close()
        return recipe
        
#test
#print(recipeQuery("pb and J"))
#input("Continue? ")
#print("Done!")
