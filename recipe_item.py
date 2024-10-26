from abc import ABC, abstractmethod
import copy


class Recipe(ABC):
    def __init__(self, name, ingredients, instructions, subrecipes=None):
        self.name = name
        self.ingredients = [{"name": ingredient[0], "quantity": ingredient[1]} for ingredient in ingredients]
        self.instructions = instructions
        self.recipe_id = RecipeIDGenerator().generate_id()
        self.subrecipes = subrecipes if subrecipes else []

    @abstractmethod
    def clone(self, **new_attributes):
        pass

    def __str__(self, indent=0):
        indent_str = ' ' * indent
        ingredient_str = ', '.join(f"{item['name']} ({item['quantity']})" for item in self.ingredients)

        subrecipes_str = ""
        if self.subrecipes:
            subrecipes_str = "\n" + "\n".join(
                subrecipe.__str__(indent=indent + 4) for subrecipe in self.subrecipes
            )

        return (f"{indent_str}ID: {self.recipe_id}, {self.name}\n"
                f"{indent_str}Ingredients: {ingredient_str}\n"
                f"{indent_str}Instructions: {self.instructions}"
                f"{subrecipes_str}")


class RecipeIDGenerator:
    _instance = None
    _id = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecipeIDGenerator, cls).__new__(cls)
        return cls._instance

    def generate_id(self):
        self._id += 1
        return self._id


class RecipeFactory:
    _created_classes = {}

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

    @staticmethod
    def _generate_clone_method():
        def clone(self, **new_attributes):
            cloned_recipe = copy.deepcopy(self)
            cloned_recipe.attributes.update(new_attributes)
            cloned_recipe.recipe_id = RecipeIDGenerator().generate_id()
            return cloned_recipe
        return clone
