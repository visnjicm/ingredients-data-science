from pprint import pprint

from CookingSystem import CookingSystem

if __name__ == "__main__":
    my_cooking = CookingSystem()
    print("Welcome to the Cooking System/App.")
    print("Here are the following kinds of recipes we currently offer:")
    print(my_cooking.all_tags)
    raw_input = input("What tag(s) would you like to search for?: ")
    include_tags = raw_input.split(',')
    my_cooking.plot_recipes_vs_ingredients_ranks(max_num_of_ingredients=10, search_tags=include_tags,
                                                 max_len_shopping_cart=50)
    pass
