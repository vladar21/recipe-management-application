import threading


class RecipeManager:
    def __init__(self):
        self.recipes = []
        self.lock = threading.Lock()

    def add_recipe(self, recipe):
        with self.lock:
            self.recipes.append(recipe)
            print(f"Added to recipe collection: {recipe}")

    def generate_recipes(self, recipe_type, name, ingredients, instructions, attributes, count, factory):
        base_recipe = factory.create_recipe(recipe_type, name, ingredients, instructions, **attributes)
        self.add_recipe(base_recipe)
        for _ in range(count - 1):
            cloned_recipe = base_recipe.clone()
            self.add_recipe(cloned_recipe)

    def show_recipes(self):
        with self.lock:
            print("\nRecipe Collection:")
            for recipe in self.recipes:
                print(recipe)
            print("-" * 30)
