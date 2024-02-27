import pickle
import ast
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
        return self.recipes[self.recipes['id'] == recipe_id].name.values[0]

    def ingredient_name(self, ingredient_id: int):
        return self.ingredients[self.ingredients['id'] == ingredient_id].replaced.values[0]

    def ingredients_names(self, ids_lst: list = []):
        lst = []
        for id in ids_lst:
            lst.append(self.ingredient_name(id))
        return lst

    def plot_recipes_vs_ingredients_ranks(self, tags: tuple = (), stop: int = -1):
        iterations = 0
        skipped = 0

        lst_ingredients_ranks = []  # list of lists, each index represents one recipe

        x_values = []
        y_values = []

        for id in self.recipes_by_tags(tags=tags)['id'].values:
            recipe_ingredients_ids = self.recipe_ingredients_ids(id)

            if len(recipe_ingredients_ids) == 0:
                skipped += 1
                continue

            else:
                recipe_ingredients_names = self.ingredients_names(recipe_ingredients_ids)
                my_ingredients_ranks = []

                for ingredient in recipe_ingredients_names:
                    my_ingredients_ranks.append(self.ingredients_sorted.index(ingredient))

                lst_ingredients_ranks.append(my_ingredients_ranks)

                x_values = x_values + lst_ingredients_ranks[iterations]
                y_values = y_values + ([iterations] * len(lst_ingredients_ranks[iterations]))

                # print()
                # print(f'Recipe Name: {self.recipe_name(id)}')
                # print(recipe_ingredients_names)
                # print(my_ingredients_ranks)
                # print(f'skipped: {skipped}')

                iterations += 1

                if iterations == stop:
                    return self._plot_y_vs_x_scatter(x_values, y_values, 'x', 'y', 'my graph')

        return self._plot_y_vs_x_scatter(x_values, y_values, 'x', 'y', 'my graph')

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
    my_cooking.plot_recipes_vs_ingredients_ranks(('main-dish', 'healthy'), 100)
