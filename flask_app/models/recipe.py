from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import recipe
from flask import flash
from flask_app.models import user, ingredient

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name'] if 'name' in data else ''
        self.description = data['description'] if 'description' in data else ''
        self.instructions = data['instructions'] if 'instructions' in data else ''
        self.user_id = data['user_id'] 
        self.img_url = data['img_url'] 
        self.total_calories = 0
        self.ingredients = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, img_url, user_id) values (%(name)s, %(description)s, %(instructions)s, %(img_url)s, %(user_id)s);'
        return connectToMySQL('xdiet').query_db(query,data)

    # @classmethod
    # def get_user_by_id_with_recipes(cls, id):
    #     query = 'SELECT * FROM recipes WHERE id = %(id)s;'
    #     data = {'id':id}
    #     results = connectToMySQL('xdiet').query_db(query, data)
    #     user = cls(results[0])
    #     user.recipes = recipe.Recipe.get_recipe_by_id(id)
    #     return user

    @classmethod
    def get_recipe_by_id(cls, id):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('xdiet').query_db(query, data)
        recipe = cls(results[0])
        return recipe

    @classmethod
    def get_recipe_by_id_with_creator(cls, id):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('xdiet').query_db(query, data)
        print(results)
        recipe = cls(results[0])
        recipe.creator = user.User.get_user_by_id(recipe.user_id)
        recipe.total_calories = ingredient.Ingredient.totals_by_recipe(recipe.id)['total_calories']
        recipe.total_proteins = ingredient.Ingredient.totals_by_recipe(recipe.id)['total_proteins']
        recipe.total_carbos = ingredient.Ingredient.totals_by_recipe(recipe.id)['total_carbos']
        recipe.total_fats = ingredient.Ingredient.totals_by_recipe(recipe.id)['total_fats']
        return recipe

    @classmethod
    def get_recipe_by_id_with_creator_json(cls, id):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('xdiet').query_db(query, data)
        recipe = results[0]
        recipe['creator_name'] = user.User.get_user_by_id(recipe['user_id']).name
        recipe['total_calories'] = ingredient.Ingredient.totals_by_recipe(recipe['id'])['total_calories']
        recipe['total_proteins'] = ingredient.Ingredient.totals_by_recipe(recipe['id'])['total_proteins']
        recipe['total_carbos'] = ingredient.Ingredient.totals_by_recipe(recipe['id'])['total_carbos']
        recipe['total_fats'] = ingredient.Ingredient.totals_by_recipe(recipe['id'])['total_fats']
        return recipe

    @classmethod
    def get_all_json(cls):
        query = 'SELECT * FROM recipes;'
        results = connectToMySQL('xdiet').query_db(query)
        recipes = []
        for recipe in results:
            recipe['creator_name'] = user.User.get_user_by_id(recipe['user_id']).name
            recipe['total_calories'] = ingredient.Ingredient.totals_by_recipe(recipe['id'])['total_calories']
            recipe['total_proteins'] = ingredient.Ingredient.totals_by_recipe(recipe['id'])['total_proteins']
            recipe['total_carbos'] = ingredient.Ingredient.totals_by_recipe(recipe['id'])['total_carbos']
            recipe['total_fats'] = ingredient.Ingredient.totals_by_recipe(recipe['id'])['total_fats']
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM recipes;'
        results = connectToMySQL('xdiet').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, img_url = %(img_url)s WHERE id = %(recipe_id)s;'    
        connectToMySQL('xdiet').query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        data = {'id': id}
        connectToMySQL('xdiet').query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash('Name has to be at least 3 characters', category='new_recipe')
            is_valid = False
        if len(recipe['description']) < 3:
            flash('Description has to be at least 3 characters', category='new_recipe')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash('Instructions have to be at least 3 characters', category='new_recipe')
            is_valid = False
        return is_valid