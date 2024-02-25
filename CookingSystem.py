import json
import pickle

import pandas as pd
from matplotlib import pyplot as plt


class CookingSystem:
    fp = ['archive/ingr_map.pkl', 'archive/RAW_recipes.csv', 'archive/PP_recipes.csv']

    def _ingr_map(self):
        with open(self.fp[0], 'rb') as file:
            ingredients = pickle.load(file)
        return ingredients

    def _raw_recipes(self):
        recipes = pd.read_csv(self.fp[1])
        return recipes

    def _tokens(self):
        tokens = pd.read_csv(self.fp[2])
        return tokens

    def check_tag(self, recipe_id: int, tag: str):
        recipes = self._raw_recipes()
        str_tag_list = recipes[recipes['id'] == recipe_id].tags.values[0]
        tag_list = str_tag_list.strip("[]").replace("'", "").split(", ")
        if tag in tag_list:
            return True
        else:
            return False

    def get_recipes_by_tags(self, tags: tuple):
        recipes = self._raw_recipes()
        return recipes[recipes['tags'].apply(lambda x: all(tag in x for tag in tags))]

    def get_ingredients_ids(self, recipe_id: int):
        tokens = self._tokens()
        var1 = tokens[tokens['id'] == recipe_id].ingredient_ids.values
        var2 = var1[0]
        var3 = json.loads(var2)
        return var3

    def get_ingredient_name(self, ingredient_id: int):
        ingredients = self._ingr_map()
        return ingredients[ingredients['id'] == ingredient_id].replaced.values[0]

    def get_recipe_name(self, recipe_id: int):
        recipes = self._raw_recipes()
        return recipes[recipes['id'] == recipe_id].name.values[0]

    def get_ingredients_names(self, ids_lst: list):
        lst = []
        for id in ids_lst:
            lst.append(self.get_ingredient_name(id))
        return lst

    def get_most_used_ingredients(self):
        ingredients_sorted = []
        ingredients = self._ingr_map()
        for ingredient in ingredients.sort_values(by='count', ascending=False).replaced.values:
            if ingredient not in ingredients_sorted:
                ingredients_sorted.append(ingredient)
        return ingredients_sorted

    @staticmethod
    def _plot_y_vs_x_scatter(x_values, y_values, x_label: str, y_label: str, title: str):
        plt.figure(figsize=(8, 6))
        plt.scatter(x_values, y_values, color='blue', alpha=1, s=3)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        plt.show()

    def plot_recipes_vs_ingredients_ranks(self, tags: tuple, stop: int):
        iterations = 0
        recipes = self.get_recipes_by_tags(tags=tags)
        recipes_ids = recipes['id'].values
        lst_ingredients_ranks = []  # list of lists, the index of each element represents the iteration number
        x_values = []
        y_values = []

        # print(ingredients_sorted[0:200])
        # testing hypothesis that score/iterations will pretty much equal to 1, or very, very close to 1
        for id in recipes_ids:
            my_ingredients = self.get_ingredients_names(self.get_ingredients_ids(id))
            my_ingredients_ranks = []

            for ingredient in my_ingredients:
                my_ingredients_ranks.append(self.get_most_used_ingredients().index(ingredient))

            lst_ingredients_ranks.append(my_ingredients_ranks)

            x_values = x_values + lst_ingredients_ranks[iterations]
            y_values = y_values + ([iterations] * len(lst_ingredients_ranks[iterations]))

            print()
            print(f'Recipe Name: {self.get_recipe_name(id)}')
            print(my_ingredients)
            print(my_ingredients_ranks)
            print()

            iterations += 1

            if iterations == stop:
                return self._plot_y_vs_x_scatter(x_values, y_values, 'x', 'y', 'my graph')

        return self._plot_y_vs_x_scatter(x_values, y_values, 'x', 'y', 'my graph')

    plot_recipes_vs_ingredients_ranks(('main-dish', 'healthy'), 5)
