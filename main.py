import pickle
import json
import pandas as pd

fp = 'archive/ingr_map.pkl'
with open(fp, 'rb') as file:
    ingredients = pickle.load(file)

fp = 'archive/RAW_recipes.csv'
recipes = pd.read_csv(fp)

fp = 'archive/PP_recipes.csv'
tokens = pd.read_csv(fp)


def filter_by_tag(tag: str):
    return recipes[recipes['tags'].apply(lambda x: tag in x)]


def get_ingredients_ids(recipe_id: int):
    return json.loads(tokens[tokens['id'] == recipe_id].ingredient_ids.values[0])


def get_ingredient_name(ingredient_id: int):
    return ingredients[ingredients['id'] == ingredient_id].replaced.values[0]


def get_recipe_name(recipe_id: int):
    return recipes[recipes['id'] == recipe_id].name.values[0]


def get_ingredients_names(ids_lst:list):
    lst = []
    for id in ids_lst:
        lst.append(get_ingredient_name(id))
    return lst


# THE CODE ABOVE TECHNICALLY ONLY NEEDS TO BE RAN ONE TIME
# FIGURE OUT HOW TO DO/IMPLEMENT THIS, SINCE IT IS SLOWING DOWN EXECUTION TIME A LOT

recipes_ids = tokens.id.values

ingredients_ids = tokens.ingredient_ids.values

my_ingredients = get_ingredients_names(get_ingredients_ids(250063))
my_recipe_name = get_recipe_name(250063)

pass
