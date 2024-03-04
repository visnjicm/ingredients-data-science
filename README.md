### Introduction
When I was in college, I wanted to cook for myself as much as possible since I didn't like eating out. I wanted my food to be fresh, healthy, and to my taste, and to be able to eat whatever I wanted. Unfortunately, I very rarely actually cooked. Takes too much time and effort to buy ingredients, prepare recipe, utensils, etc. I asked myself the question: What combination of ingredients can I buy that will ensure I can cook X many recipes,  and have X many servings of each? The reason this question is so important to me, is because once I can answer this question, theoretically, all I need to do is go buy the ingredients from the store (that this software tells me to buy), and thats it!

### Analysis
General plot (zoomed out):
![plot_feb232024](https://github.com/visnjicm/ingredients-data-science/assets/126916558/3a3c6575-9a9d-4349-9015-0a4243c1908c)

The deception of this plot, is in the fact that it appears as if there are some ingredients that appear in almost every single recipe (the completely solid lines at rank 0, 3, 5, 6, 7, and 34).

General plot (deception):
![Screenshot from 2024-03-04 15-24-57](https://github.com/visnjicm/ingredients-data-science/assets/126916558/542e2d18-650b-4002-9bee-b52f7af99052)

*The denser the lines in the plot, the more frequently the that ingredient rank appears in the recipes. For this example, 0,3,5,6,7,and 34, which when decoded are, salt, onion, garlic clove, something else, and chicken breast. It makes intuitive sense that these appear the most often in 'main-dish' and 'healthy' recipes*

However, on closer inspection, you see that this is just an illusion, the true nature reveals itself when you zoom in...

General plot (zoomed in):
![Screenshot from 2024-03-04 16-08-14](https://github.com/visnjicm/ingredients-data-science/assets/126916558/32de9d9b-ae8e-495f-90b9-ee17f467bd78)

There is no repeating pattern, the data is inherently scattered as you can see. (If you don't believe me, zoom in on any part of the plot and you will see.)





### Sources

https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions




