import pickle
import json

import pandas
import pandas as pd

fp = 'archive/ingr_map.pkl'
with open(fp, 'rb') as file:
    ingredients = pickle.load(file)

fp = 'archive/RAW_recipes.csv'
recipes = pd.read_csv(fp)

fp = 'archive/PP_recipes.csv'
tokens = pd.read_csv(fp)


def check_tag(recipe_id: int, tag: str):
    str_tag_list = recipes[recipes['id'] == recipe_id].tags.values[0]
    tag_list = str_tag_list.strip("[]").replace("'", "").split(", ")
    if tag in tag_list:
        return True
    else:
        return False


def get_recipes_by_tag(tag: str):
    return recipes[recipes['tags'].apply(lambda x: tag in x)]


def get_ingredients_ids(recipe_id: int):
    return json.loads(tokens[tokens['id'] == recipe_id].ingredient_ids.values[0])


def get_ingredient_name(ingredient_id: int):
    return ingredients[ingredients['id'] == ingredient_id].replaced.values[0]


def get_recipe_name(recipe_id: int):
    return recipes[recipes['id'] == recipe_id].name.values[0]


def get_ingredients_names(ids_lst: list):
    lst = []
    for id in ids_lst:
        lst.append(get_ingredient_name(id))
    return lst


# THE CODE ABOVE TECHNICALLY ONLY NEEDS TO BE RAN ONE TIME
# FIGURE OUT HOW TO DO/IMPLEMENT THIS, SINCE IT IS SLOWING DOWN EXECUTION TIME A LOT

recipes_ids = tokens.id.values

ingredients_ids = tokens.ingredient_ids.values

var4 = ingredients.sort_values(by='count', ascending=False).replaced.values

ingredients_sorted = []

for ingredient in var4:
    if ingredient not in ingredients_sorted:
        ingredients_sorted.append(ingredient)

my_ingredients = get_ingredients_names(get_ingredients_ids(424415))
my_recipe_name = get_recipe_name(424415)

var = get_recipes_by_tag('main-dish')

var3 = check_tag(424415, 'main-dish')

for id in recipes_ids:
    if check_tag(id, 'main-dish') and check_tag(id, 'healthy'):
        my_ingredients = get_ingredients_names(get_ingredients_ids(id))
        my_recipe_name = get_recipe_name(id)
        my_ingredients_ids = get_ingredients_ids(id)
        my_ingredients_ranks = []

        for ingredient in my_ingredients:
            var5 = ingredients[ingredients['processed'] == ingredient].replaced.values[0]
            my_ingredients_ranks.append(ingredients_sorted.index(var5))
            pass
        pass

pass
