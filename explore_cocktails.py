# explore cocktails recipe dataset

import pandas as pd
import numpy as np
import re

import plotly
from plotly.graph_objs import Scatter, Layout

# show whole columns without display truncation
pd.set_option('display.max_colwidth', -1)

# dataframe of strings
data = pd.read_pickle("cocktails_thecocktaildb.pickle")

# extract only ingredients, no dosage
replace_regexp = "\soz|parts?|tsp|tblsp|chunks?|dashes?|slices?|\scups?|\scl|\d-\d|[0-9]|drops?|\sL\s|dl|\sgr\s|qt|/|to\staste|\slb"
data["ingredients_nodosage"]  = data["ingredients"].replace(to_replace=replace_regexp,value="", inplace=False, regex=True)

# keep only names of ingredients
def split_str(l):
    
    ll = l.lower().split(",")
    return [re.sub("\W", "", ingredient) for ingredient in ll]

data["ingredients_list"] = data["ingredients_nodosage"].apply(split_str)

data.head(5)

data.to_csv("cocktails_thecocktaildb_ingredients_split.csv", sep='#', columns=["name", "ingredients_list", "instructions"], header=True, index=False, mode='w', encoding="utf8")
