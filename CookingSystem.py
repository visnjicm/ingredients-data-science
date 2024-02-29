import pickle
import ast
import random

import pandas as pd
from matplotlib import pyplot as plt


class CookingSystem:
    fp = ['archive/ingr_map.pkl', 'archive/RAW_recipes.csv']

    def __init__(self):

        # initialize ingredients dataframe
        with open(self.fp[0], 'rb') as file:
            self.ingredients = pickle.load(file)

        # initialize recipes dataframe
        self.recipes = pd.read_csv(self.fp[1])

        self.ingredients_sorted = []
        for ingredient in self.ingredients.sort_values(by='count', ascending=False).replaced.values:
            if ingredient not in self.ingredients_sorted:
                self.ingredients_sorted.append(ingredient)

        self.tags = self._tags()

        print(self.tags)

        pass

    def _tags(self):
        tags_set = set()
        str_tags_lst = self.recipes['tags'].values
        for str_tags in str_tags_lst:
            tags = ast.literal_eval(str_tags)
            tags_set.update(tags)
        return tags_set

    def recipes_by_tags(self, tags: tuple) -> pd.DataFrame:
        """
        Return a pandas dataframe object that contains only the recipes which include in their tags field, the
        tags specified by the user as an input parameter. If the input parameter is an empty tuple, then the
        function just returns the original recipes dataframe.
        """
        if tags is None:
            return self.recipes
        else:
            return self.recipes[self.recipes['tags'].apply(lambda x: all(tag in x for tag in tags))]

    def recipe_ingredients_ids(self, recipe_id: int) -> list:
        """
        Returns a list of all the id's for all the ingredients of the recipe id specified as the input parameter.
        """

        ingredient_ids = []
        ingredient_names = ast.literal_eval(
            self.recipes[self.recipes['id'] == recipe_id].ingredients.values[0])

        for ingredient_name in ingredient_names:
            # if the ingredient_name cannot be found, return empty list to tell the program this
            if self.ingredients[self.ingredients['raw_ingr'] == ingredient_name].empty:
                return []
            else:
                ingredient_id = self.ingredients[self.ingredients['raw_ingr'] == ingredient_name].id.values[0]
            ingredient_ids.append(ingredient_id)

        return ingredient_ids

    def recipe_name(self, recipe_id: int):
        """
        Returns the recipe name of the recipe specified by its id as input parameter to this function.
        """
        return self.recipes[self.recipes['id'] == recipe_id].name.values[0]

    def ingredient_name(self, ingredient_id: int):
        """
        Returns the name of the ingredient with the id specified as the input parameter to this function.
        """
        return self.ingredients[self.ingredients['id'] == ingredient_id].replaced.values[0]

    def ingredients_names(self, ids_lst: list = []):
        """
        Converts a ingredient id's list to a ingredient name's list.
        """
        lst = []
        for id in ids_lst:
            lst.append(self.ingredient_name(id))
        return lst

    def num_of_ingredients(self, recipe_id: int):
        return self.recipes[self.recipes['id'] == recipe_id].n_ingredients.values.max()

    def plot_recipes_vs_ingredients_ranks(self, tags: tuple = (), stop: int = -1):
        """
        Generate a recipes vs ingredients ranks plot for all the recipes (in the CookingSystem database) which contain
        at least the tags specified in the tags tuple input parameter to this function. The user of this function can
        also specify stop condition to indiciate at what iteration they would like the plot to stop. Plot will continue
        until all recipes have been graphed, if no stop condition is input.
        """
        iterations = 0

        lst_ingredients_ranks = []  # list of lists, each index represents one recipe

        x_values = []
        y_values = []

        shopping_cart = set()

        my_var = self.recipes_by_tags(tags)

        lst_recipes = self.recipes_by_tags(tags=tags)['id'].values.tolist()

        lst_recipes = random.sample(lst_recipes, len(lst_recipes))

        for id in lst_recipes:
            recipe_ingredients_ids = self.recipe_ingredients_ids(id)

            if len(recipe_ingredients_ids) == 0:
                continue

            if self.num_of_ingredients(id) > 8:
                continue

            else:
                recipe_ingredients_names = self.ingredients_names(recipe_ingredients_ids)
                my_ingredients_ranks = []

                for ingredient in recipe_ingredients_names:
                    my_ingredients_ranks.append(self.ingredients_sorted.index(ingredient))

                if any(num > 1000 for num in my_ingredients_ranks):
                    continue

                if all(num in my_ingredients_ranks for num in []):
                    lst_ingredients_ranks.append(my_ingredients_ranks)
                else:
                    continue

                x_values = x_values + lst_ingredients_ranks[iterations]
                y_values = y_values + ([iterations] * len(lst_ingredients_ranks[iterations]))

                iterations += 1
                shopping_cart.update(recipe_ingredients_names)
                print(self.recipe_name(id))

                if iterations == stop:
                    print(shopping_cart)
                    print(len(shopping_cart))
                    return self._plot_y_vs_x_scatter(x_values,
                                                     y_values,
                                                     'Ingredient Rank',
                                                     'Recipe #',
                                                     'Recipes vs Ingredient Ranks')

        print(shopping_cart)
        print(len(shopping_cart))
        return self._plot_y_vs_x_scatter(x_values,
                                         y_values,
                                         'Ingredient Rank',
                                         'Recipe #',
                                         'Recipes vs Ingredient Ranks')

    @staticmethod
    def _plot_y_vs_x_scatter(x_values, y_values, x_label: str, y_label: str, title: str):
        plt.figure(figsize=(8, 6))
        plt.scatter(x_values, y_values, color='blue', alpha=1, s=3)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        plt.show()

    @staticmethod
    def df_to_csv(df: pd.DataFrame):
        df.to_csv('ingredients.csv')


if __name__ == "__main__":
    my_cooking = CookingSystem()
    my_cooking.df_to_csv(my_cooking.ingredients)
    my_cooking.plot_recipes_vs_ingredients_ranks(('quail'), stop=10)
