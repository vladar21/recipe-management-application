# Recipe Management Application

Hi!

My name is Vladyslav Rastvorov, I am a student of CO.SDH3-A group.

Here is a step-by-step explanation of my code for the Recipe Management Application assignment:
Create a Recipe Management Application using the Factory Design Pattern, Prototype Design
Pattern, and multithreading in Python.

## Overview

This code implements Factory Design Pattern, Prototype Design Pattern, and multithreading in Python. Each recipe has a unique ID, generated with a singleton-based RecipeIDGenerator. The code supports creating recipes with ingredients and nested sub-recipes.

The code is divided into three files:

1) ```recipe_item.py``` — Defines the base classes for recipes, the ID generator, and a factory for creating recipe instances.

2) ```recipe_manager.py``` — Manages the collection of recipes with thread-safe operations.

3) ```main.py``` — Demonstrates the functionality by creating and managing multiple recipes with multithreading.

## File: recipe_item.py

This file defines the base ```Recipe``` class, the ```RecipeFactory```, and the ```RecipeIDGenerator``` for unique ```recipe IDs```.

1) Imports necessary modules for abstract classes and copying:
```python
from abc import ABC, abstractmethod
import copy
```

2) Defines ```Recipe``` as an abstract base class.
```python
class Recipe(ABC):
```

3) Initializes recipe attributes, including ```name```, ```ingredients```, ```instructions```, and optional sub-recipes:
```python
def __init__(self, name, ingredients, instructions, subrecipes=None):
    self.name = name
    self.ingredients = [{"name": ingredient[0], "quantity": ingredient[1]} for ingredient in ingredients]
    self.instructions = instructions
    self.recipe_id = RecipeIDGenerator().generate_id()  # Generates unique ID
    self.subrecipes = subrecipes if subrecipes else []  # Stores nested recipes if any

```

4) Declares ```clone``` as an abstract method to be implemented by subclasses:
```python
@abstractmethod
def clone(self, **new_attributes):
    pass
```

5) Creates a string representation of the recipe, including sub-recipes:
```python
def __str__(self, indent=0):
    indent_str = ' ' * indent
    ingredient_str = ', '.join(f"{item['name']} ({item['quantity']})" for item in self.ingredients)
    subrecipes_str = "\n" + "\n".join(
        subrecipe.__str__(indent=indent + 4) for subrecipe in self.subrecipes) if self.subrecipes else ""
    return f"{indent_str}ID: {self.recipe_id}, {self.name}\n{indent_str}Ingredients: {ingredient_str}\n{indent_str}Instructions: {self.instructions}{subrecipes_str}"
```

6)  Defines RecipeIDGenerator as a singleton to manage unique IDs:
```python
class RecipeIDGenerator:
```

7) Holds the singleton instance and ID counter:
```python
_instance = None
_id = 0
```

8) Ensures only one instance of ```RecipeIDGenerator```:
```python
def __new__(cls):
    if cls._instance is None:
        cls._instance = super(RecipeIDGenerator, cls).__new__(cls)
    return cls._instance

```

9) Generates and returns a unique ID each time it’s called:
```python
def generate_id(self):
    self._id += 1
    return self._id
```

10) Define ```RecipeFactory```, which will create instances of ```Recipe``` subclasses dynamically
```python
class RecipeFactory:
    _created_classes = {}
```

11) create_recipe static method creates a new class if it doesn’t exist and then instantiates it.
```python
@staticmethod
def create_recipe(recipe_type, name, ingredients, instructions, subrecipes=None, **attributes):
    if recipe_type not in RecipeFactory._created_classes:
        RecipeFactory._created_classes[recipe_type] = type(
            recipe_type,
            (Recipe,),
            {
                "clone": RecipeFactory._generate_clone_method()
            }
        )
    recipe_class = RecipeFactory._created_classes[recipe_type]
    return recipe_class(name, ingredients, instructions, subrecipes, **attributes)
```

12) ```clone``` method is generated dynamically, enabling each instance to copy itself with a new ID.
```pytho
@staticmethod
def _generate_clone_method():
    def clone(self, **new_attributes):
        cloned_recipe = copy.deepcopy(self)
        cloned_recipe.attributes.update(new_attributes)
        cloned_recipe.recipe_id = RecipeIDGenerator().generate_id()
        return cloned_recipe
    return clone
```

## File: recipe_manager.py

This file contains ```RecipeManager```, which manages recipes with thread safety.

1) Import threading for multithreading support
```python
import threading
```

2) Define ```RecipeManager``` to manage recipes in a thread-safe way.
```python
class RecipeManager:
```

3) initializes an empty recipe list and a lock for thread safety.
```python
def __init__(self):
    self.recipes = []
    self.lock = threading.Lock()
```

4) adds a recipe to the collection in a thread-safe way.
```python
def add_recipe(self, recipe):
    with self.lock:
        self.recipes.append(recipe)
        print(f"Added to recipe collection: {recipe}")
```

5) method generates multiple recipes and clones, adding them to the collection.
```python
def generate_recipes(self, recipe_type, name, ingredients, instructions, attributes, count, factory):
    base_recipe = factory.create_recipe(recipe_type, name, ingredients, instructions, **attributes)
    self.add_recipe(base_recipe)
    for _ in range(count - 1):
        cloned_recipe = base_recipe.clone()
        self.add_recipe(cloned_recipe)
        time.sleep(random.random())
```

6) displays the full list of recipes, ensuring thread safety.
```python
def show_recipes(self):
    with self.lock:
        print("\nRecipe Collection:")
        for recipe in self.recipes:
            print(recipe)
        print("-" * 30)
```

## File: main.py

This file demonstrates the Recipe Management System in action.

1) Import required modules for threading, ```RecipeManager```, and ```RecipeFactory```.
```python
import threading
from recipe_manager import RecipeManager
from recipe_item import RecipeFactory
```

2) function, which creates a cake recipe with nested sub-recipes for ```frosting``` and ```cake base```.
```python
def create_cake_recipe():
    print("Starting thread for Layer Cake")
    frosting = factory.create_recipe('Dessert', 'Frosting', [('sugar', '1 cup'), ('butter', '1/2 cup'), ('vanilla', '1 tsp')],
                                     'Mix all ingredients until smooth.')
    cake_base = factory.create_recipe('Dessert', 'Cake Base', [('flour', '2 cups'), ('sugar', '1 cup'), ('eggs', '3')],
                                      'Mix ingredients and bake at 350°F for 30 minutes.')
    cake = factory.create_recipe('Dessert', 'Layer Cake', [('milk', '1 cup'), ('baking powder', '1 tbsp')],
                                 'Prepare the layers and frost each layer.', subrecipes=[frosting, cake_base])
    recipe_manager.add_recipe(cake)
    print("Finished thread for Layer Cake")
```

3) function, which creates a lemonade recipe in another thread.
```python
def create_lemonade_recipe():
    print("Starting thread for Lemonade")
    lemonade = factory.create_recipe('Beverage', 'Lemonade', [('water', '2 cups'), ('lemon', '1 whole'), ('sugar', '2 tbsp')],
                                     'Mix ingredients and serve cold.')
    recipe_manager.add_recipe(lemonade)
    print("Finished thread for Lemonade")
```

4) Initialize ```RecipeManager``` and ```RecipeFactory``` instances.
```python
if __name__ == "__main__":
    recipe_manager = RecipeManager()
    factory = RecipeFactory()
```

5) Create and start threads for ```create_cake_recipe``` and ```create_lemonade_recipe```.
```python
thread1 = threading.Thread(target=create_cake_recipe)
thread2 = threading.Thread(target=create_lemonade_recipe
thread1.start()
thread2.start()
```

6) Waits for threads to finish before proceeding
```python
thread1.join()
thread2.join()
```

7) Displays all recipes in the ```recipe_manager``` collection
```python
recipe_manager.show_recipes()
```

## Result
```bash
$ python main.py
Starting thread for Layer Cake
Added to recipe collection: ID: 3, Layer Cake
Ingredients: milk (1 cup), baking powder (1 tbsp)
Instructions: Prepare the layers and frost each layer.
    ID: 1, Frosting
    Ingredients: sugar (1 cup), butter (1/2 cup), vanilla (1 tsp)
    Instructions: Mix all ingredients until smooth.
    ID: 2, Cake Base
    Ingredients: flour (2 cups), sugar (1 cup), eggs (3)
    Instructions: Mix ingredients and bake at 350°F for 30 minutes.
Starting thread for Lemonade
Finished thread for Layer Cake
Added to recipe collection: ID: 4, Lemonade
Ingredients: water (2 cups), lemon (1 whole), sugar (2 tbsp)
Instructions: Mix ingredients and serve cold.
Finished thread for Lemonade

Recipe Collection:
ID: 3, Layer Cake
Ingredients: milk (1 cup), baking powder (1 tbsp)
Instructions: Prepare the layers and frost each layer.
    ID: 1, Frosting
    Ingredients: sugar (1 cup), butter (1/2 cup), vanilla (1 tsp)
    Instructions: Mix all ingredients until smooth.
    ID: 2, Cake Base
    Ingredients: flour (2 cups), sugar (1 cup), eggs (3)
    Instructions: Mix ingredients and bake at 350°F for 30 minutes.
ID: 4, Lemonade
Ingredients: water (2 cups), lemon (1 whole), sugar (2 tbsp)
Instructions: Mix ingredients and serve cold.
------------------------------
```

That's all. Thank you.