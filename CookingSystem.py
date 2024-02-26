import json
import pickle
import ast

import pandas as pd
from matplotlib import pyplot as plt


class CookingSystem:
    # recipes_ids = get_recipes_by_tags(tags=('main-dish', 'healthy'))['id'].values
    #
    # ingredients_ids = tokens.ingredient_ids.values
    #
    # var4 = df_ingredients.sort_values(by='count', ascending=False).replaced.values
    # my_ingredients = get_ingredients_names(get_ingredients_ids(424415))

    # var = get_rec??ipes_by_tag('main-dish')
    #
    # var7 = get_recipes_by_tag('breakfast')
    #
    # var3 = check_tag(424415, 'main-dish')

    # my_recipe_name = get_recipe_name(424415)

    fp = ['archive/ingr_map.pkl', 'archive/RAW_recipes.csv', 'archive/PP_recipes.csv']

    def __init__(self):
        self.df_ingredients = self._df_ingr_map()
        self.df_recipes = self._df_raw_recipes()
        self.most_used_ingredients = self._most_used_ingredients()

    @staticmethod
    def df_to_csv(df:pd.DataFrame):
        df.to_csv('ingredients.csv')


    def _df_ingr_map(self):
        with open(self.fp[0], 'rb') as file:
            return pickle.load(file)

    def _df_raw_recipes(self):
        return pd.read_csv(self.fp[1])

    def _df_tokens(self):
        return pd.read_csv(self.fp[2])

    def _most_used_ingredients(self):
        ingredients_sorted = []
        ingredients = self._df_ingr_map()
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

    def check_tag(self, recipe_id: int, tag: str):
        str_tag_list = self.df_recipes[self.df_recipes['id'] == recipe_id].tags.values[0]
        tag_list = str_tag_list.strip("[]").replace("'", "").split(", ")
        if tag in tag_list:
            return True
        else:
            return False

    def get_recipes_by_tags(self, tags: tuple):
        if tags is None:
            return self.df_recipes
        else:
            return self.df_recipes[self.df_recipes['tags'].apply(lambda x: all(tag in x for tag in tags))]

    def get_recipe_name(self, recipe_id: int):
        return self.df_recipes[self.df_recipes['id'] == recipe_id].name.values[0]

    def get_ingredients_ids(self, recipe_id: int) -> list:
        recipe_ingredient_ids = []
        var1 = self.df_recipes[self.df_recipes['id'] == recipe_id].ingredients.values
        # print(self.get_recipe_name(recipe_id))
        var2 = var1[0]
        recipe_ingredients_names = ast.literal_eval(var2)
        pass
        for ingredient_name in recipe_ingredients_names:
            df_row_match = self.df_ingredients[self.df_ingredients['raw_ingr'] == ingredient_name]
            if df_row_match.empty:
                return []
            else:
                ingredient_id = df_row_match.id.values[0]
            recipe_ingredient_ids.append(ingredient_id)

        pass
        return recipe_ingredient_ids

    def get_ingredient_name(self, ingredient_id: int):
        return self.df_ingredients[self.df_ingredients['id'] == ingredient_id].replaced.values[0]

    def get_ingredients_names(self, ids_lst: list = []):
        lst = []
        for id in ids_lst:
            lst.append(self.get_ingredient_name(id))
        return lst

    def plot_recipes_vs_ingredients_ranks(self, tags:tuple = (), stop:int = -1):
        iterations = 0
        skipped = 0

        self.df_recipes = self.get_recipes_by_tags(tags=tags)
        self.recipes_ids = self.df_recipes['id'].values
        self.lst_ingredients_ranks = []  # list of lists, the index of each element represents the iteration number

        x_values = []
        y_values = []

        # print(ingredients_sorted[0:200])
        # testing hypothesis that score/iterations will pretty much equal to 1, or very, very close to 1
        for id in self.recipes_ids:
            recipe_ingredients_ids = self.get_ingredients_ids(id)
            if len(recipe_ingredients_ids) == 0:
                skipped += 1
                continue

            else:
                my_ingredients = self.get_ingredients_names(recipe_ingredients_ids)
                my_ingredients_ranks = []

                for ingredient in my_ingredients:
                    my_ingredients_ranks.append(self.most_used_ingredients.index(ingredient))

                self.lst_ingredients_ranks.append(my_ingredients_ranks)

                x_values = x_values + self.lst_ingredients_ranks[iterations]
                y_values = y_values + ([iterations] * len(self.lst_ingredients_ranks[iterations]))

                print()
                print(f'Recipe Name: {self.get_recipe_name(id)}')
                print(my_ingredients)
                print(my_ingredients_ranks)
                print(f'skipped: {skipped}')

                iterations += 1

                if iterations == stop:
                    return self._plot_y_vs_x_scatter(x_values, y_values, 'x', 'y', 'my graph')

        return self._plot_y_vs_x_scatter(x_values, y_values, 'x', 'y', 'my graph')


if __name__ == "__main__":
    my_cooking = CookingSystem()
    my_cooking.df_to_csv(my_cooking.df_ingredients)
    my_cooking.plot_recipes_vs_ingredients_ranks(('dessert'), 1000)
