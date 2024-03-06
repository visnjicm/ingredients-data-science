import pickle
import ast
import random

import pandas as pd
from matplotlib import pyplot as plt


class CookingSystem:
    fp = ['archive/ingr_map.pkl', 'archive/RAW_recipes.csv']

    def __init__(self):

        with open(self.fp[0], 'rb') as file:
            self.ingredients = pickle.load(file)

        self.recipes = pd.read_csv(self.fp[1])

        self.ingredients_sorted = []
        for ingredient in self.ingredients.sort_values(by='count', ascending=False).replaced.values:
            if ingredient not in self.ingredients_sorted:
                self.ingredients_sorted.append(ingredient)

        self.all_tags = self._all_tags()

        pass

    def _all_tags(self):
        tags_set = set()
        str_tags_lst = self.recipes['tags'].values
        for str_tags in str_tags_lst:
            tags = ast.literal_eval(str_tags)
            tags_set.update(tags)
        return tags_set

    def recipes_by_tags(self, tags: list) -> pd.DataFrame:
        if tags is None or []:
            return self.recipes
        else:
            drop_lst = []
            for index, row in self.recipes.iterrows():
                # should I change this to any, or keep it all?
                if all(tag in ast.literal_eval(row.tags) for tag in tags):
                    # keep row
                    continue
                else:
                    # discard row
                    drop_lst.append(index)

            return self.recipes.drop(drop_lst)

    def recipe_ingredients_ids(self, recipe_id: int) -> list:

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

    def recipe_name(self, recipe_id: int) -> str:
        """
        Returns the recipe name of the recipe specified by its id as input parameter to this function.
        """
        return self.recipes[self.recipes['id'] == recipe_id].name.values[0]

    def recipe_tags(self, recipe_id: int) -> list:
        return ast.literal_eval(self.recipes[self.recipes['id'] == recipe_id].tags.values[0])

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

    def plot_recipes_vs_ingredients_ranks(self, max_num_of_ingredients: int = 9999999,
                                          rank_upper_bound: int = 9999999,
                                          include_tags: list = [],
                                          omit_tags: list = [],
                                          can_include: list = [],
                                          must_include: list = [],
                                          omit_strings: list = [],
                                          max_len_shopping_cart=9999999,
                                          stop: int = -1) -> None:
        """
        Generate a recipes vs ingredients ranks plot for all the recipes (in the CookingSystem database) which
        contain at least the all_tags specified in the all_tags tuple input parameter to this function. The user of this
        function can also specify stop condition to indicate at what iteration they would like the plot to stop.
        Plot will continue until all recipes have been graphed, if no stop condition is input.
        :param max_num_of_ingredients: Max num of ingredients that any recipe can have.
        :param rank_upper_bound: Upper bound on ingredient rank.
        :param include_tags: Recipes returned will contain at least these all_tags.
        :param can_include: Recipes returned will contain at least the ingredients, with ranks specified here.
        :param stop: Function will return/stop after this many recipes have been "found".
        :return: None
        """

        iterations = 0

        lst_ingredients_ranks = []  # list of lists, each index represents one recipe

        x_values = []
        y_values = []

        shopping_cart = set()

        # my_var = self.recipes_by_tags(all_tags)

        lst_recipes = self.recipes_by_tags(tags=include_tags)['id'].values.tolist()

        lst_recipes = random.sample(lst_recipes, len(lst_recipes))

        for id in lst_recipes:
            recipe_ingredients_ids = self.recipe_ingredients_ids(id)

            # skip empty recipes
            if len(recipe_ingredients_ids) == 0:
                continue

            if self.num_of_ingredients(id) > max_num_of_ingredients:
                continue

            if any(string in self.recipe_name(id) for string in omit_strings):
                continue

            if any(tag in self.recipe_tags(id) for tag in omit_tags):
                continue

            else:
                recipe_ingredients_names = self.ingredients_names(recipe_ingredients_ids)
                my_ingredients_ranks = []

                for ingredient in recipe_ingredients_names:
                    my_ingredients_ranks.append(self.ingredients_sorted.index(ingredient))

                # max recipe rank
                if any(num > rank_upper_bound for num in my_ingredients_ranks):
                    continue

                if (any(num in my_ingredients_ranks for num in can_include) or can_include == []) and (all(
                        num in my_ingredients_ranks for num in must_include) or must_include == []):
                    lst_ingredients_ranks.append(my_ingredients_ranks)
                else:
                    continue

                x_values = x_values + lst_ingredients_ranks[iterations]
                y_values = y_values + ([iterations] * len(lst_ingredients_ranks[iterations]))

                iterations += 1
                shopping_cart.update(recipe_ingredients_names)

                print()
                print(f"Recipe Name: {self.recipe_name(id)}")
                print(f"Recipe Tags: {self.recipe_tags(id)}")
                print(f"Recipe Ingredients: {self.ingredients_names(self.recipe_ingredients_ids(id))}")
                print()

                if len(shopping_cart) >= max_len_shopping_cart:
                    break

                if iterations == stop:
                    break

        print(f"num of recipes: {iterations}")
        print(shopping_cart)
        print(len(shopping_cart))
        return None

    @staticmethod
    def _plot_y_vs_x_scatter(x_values, y_values, x_label: str, y_label: str, title: str):
        plt.figure(figsize=(8, 6))
        plt.scatter(x_values, y_values, color='blue', alpha=1, s=0.5)
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
    # my_cooking.df_to_csv(my_cooking.ingredients)
    # print([my_cooking.ingredients_sorted[value] for value in [0, 3, 5, 6, 7, 34]])
    my_cooking.plot_recipes_vs_ingredients_ranks(include_tags=['breakfast'],
                                                 omit_strings=['sauce', 'syrup'],
                                                 max_len_shopping_cart=50,
                                                 omit_tags=['kid-friendly'])
