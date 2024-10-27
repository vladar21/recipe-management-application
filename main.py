import threading
from recipe_manager import RecipeManager
from recipe_item import RecipeFactory


def create_cake_recipe():
    print("Starting thread for Layer Cake")
    frosting = factory.create_recipe('Dessert', 'Frosting', [('sugar', '1 cup'), ('butter', '1/2 cup'), ('vanilla', '1 tsp')], 'Mix all ingredients until smooth.')
    cake_base = factory.create_recipe('Dessert', 'Cake Base', [('flour', '2 cups'), ('sugar', '1 cup'), ('eggs', '3')], 'Mix ingredients and bake at 350°F for 30 minutes.')
    cake = factory.create_recipe('Dessert', 'Layer Cake', [('milk', '1 cup'), ('baking powder', '1 tbsp')], 'Prepare the layers and frost each layer.', subrecipes=[frosting, cake_base])

    recipe_manager.add_recipe(cake)
    print("Finished thread for Layer Cake")


def create_lemonade_recipe():
    print("Starting thread for Lemonade")
    lemonade = factory.create_recipe('Beverage', 'Lemonade', [('water', '2 cups'), ('lemon', '1 whole'), ('sugar', '2 tbsp')], 'Mix ingredients and serve cold.')
    recipe_manager.add_recipe(lemonade)
    print("Finished thread for Lemonade")


if __name__ == "__main__":
    recipe_manager = RecipeManager()
    factory = RecipeFactory()

    # Create threads for each recipe
    thread1 = threading.Thread(target=create_cake_recipe)
    thread2 = threading.Thread(target=create_lemonade_recipe)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

    # Display the full recipe collection
    recipe_manager.show_recipes()
