# load all the cocktails recipes from the CocktailDB API

import numpy as np
import requests
import pandas as pd

# return lists of names of cocktails matching query
url_non_alcoholic = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic"
url_alcoholic = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Alcoholic"

# Get list of cocktails ids:
def get_ids(url):
    response = requests.post(url).json()
    return [response["drinks"][i]["idDrink"] for i in range(len(response["drinks"]))]

cocktails_ids = get_ids(url_non_alcoholic) +  get_ids(url_alcoholic)

print("number of cocktails: {}".format(len(cocktails_ids))) # ?? should be 573

recipes = []

for cocktail_id in cocktails_ids:
    url =  "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i="+str(cocktail_id)
    response = requests.post(url).json()
    name = response["drinks"][0]["strDrink"]
    dosages = [v for k,v in response["drinks"][0].iteritems() if ('Measure' in k and v and not v.isspace())]
    ingredients = [v for k,v in response["drinks"][0].iteritems() if ('Ingredient' in k and v and not v.isspace())]
    ingredients_dosage = [dose.strip() + " " + ingredient.strip() for (dose,ingredient) in zip(dosages, ingredients)]
#    recipes.append(name + ": " + ", ".join(ingredients_dosage) + ". " + response["drinks"][0]["strInstructions"])
    clean_instructions = response["drinks"][0]["strInstructions"].replace('"','').replace('\n',' ').replace("'","")
    recipes.append([name, ", ".join(ingredients_dosage), clean_instructions])

# write as text file for learning
with open("cocktails_thecocktaildb.txt", mode="w") as f:
    for s in recipes:
        ss = "%s\n" % "#".join(s)
        f.write(ss.encode('utf8'))

# write as dataframe for exploring
df = pd.DataFrame(recipes, columns=["name", "ingredients", "instructions"])
print(df.head())
df.to_pickle("cocktails_thecocktaildb.pickle")
