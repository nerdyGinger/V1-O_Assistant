"""
Program: recipeDatabase.py
Author: nerdyGinger
Connection to Heroku database for updating and querying recipes.
"""

import os, psycopg2, urllib.parse
from constants import *

def recipeResponse(data):
    if data == "No recipe found.":
        return { "fulfillmentText": data,
                 "source": "recipeDatabase" }
    return { "fulfillmentText": ("I found the recipe for " + data[0] +
                                 ". " + str(data[1]) +
                                 " It takes " + str(data[2]) + " to prepare " +
                                 "and makes " + str(data[3]) + ". "),
             "source": "recipeDatabase" }

def nextStep(data, contexts, index):
    if int(index) == len(data[5])-1:
        return { "fulfillmentText": "There are no more steps.",
                 "source": "recipeDatabase" }
    return { "fulfillmentText": data[5][int(index)+1],
             "source": "recipeDatabase",
             "outputContexts": [
                 {"name": contexts[0].get("name"),
                 "lifespanCount": contexts[0].get("lifespanCount"),
                 "parameters": {
                     "count": str(int(index)+1)
                     }}]}

def repeatStep(data, index):
    if int(index) < 0:
        index = 0
    return { "fulfillmentText": data[5][int(index)],
             "source": "recipeDatabase" }

def prevStep(data, contexts, index):
    if int(index) <= 0:
        return { "fulfillmentText": "There are no previous steps.",
                 "source": "recipeDatabase" }
    return { "fulfillmentText": data[5][int(index)-1],
             "source": "recipeDatabase",
             "outputContexts": [
                 {"name": contexts[0].get("name"),
                 "lifespanCount": contexts[0].get("lifespanCount"),
                 "parameters": {
                     "count": str(int(index)-1)
                     }}]}

def ingredients(data):
    return { "fulfillmentText": str(data[4]),
             "source": "recipeDatabase" }

def allRecipes():
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    lyst = "No recipes found"
    try:
        cursor = connection.cursor()
        cursor.execute('''SELECT name FROM recipies;''')
        lyst = str(cursor.fetchall())
    except:
        print("Issue querying database!")
    finally:
        connection.close()
        lyst = lyst.replace(",), (", ", ")
        lyst = lyst.replace("[(", "")
        lyst = lyst.replace(",)]", "")
        return { "fulfillmentText": "Here are the recipe I found: " + lyst,
                 "source": "recipeDatabase" }

def recipeQuery(recipeName):
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    recipe = ["No recipe found"]
    recipeName = recipeName.replace("&", " and ")
    recipeName = recipeName.replace("1", "one")
    recipeName = recipeName.replace("2", "two")
    recipeName = recipeName.replace("3", "three")
    recipeName = recipeName.replace("4", "four")
    recipeName = recipeName.replace("5", "five")
    recipeName = recipeName.replace("6", "six") 
    recipeName = recipeName.replace("7", "seven") 
    recipeName = recipeName.replace("8", "eight") 
    recipeName = recipeName.replace("9", "nine") 

    try:
        cursor = connection.cursor()
        cursor.execute('''SELECT name, description, preptime, yield, ingredients, directions FROM recipies
                          WHERE LOWER(name) = LOWER(%s);''', (recipeName,))
        recipe = (cursor.fetchall())
    except:
        print("Issue querying database!")
    finally:
        connection.close()
        if recipe == []:
            return "No recipe found for " + recipeName + "."
        return recipe[0]
        
#test
#print(allRecipes())
#input("Continue? ")
#print("Done!")
