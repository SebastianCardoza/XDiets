from dataclasses import dataclass
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import food
from flask import flash

class Ingredient:
    def __init__(self, data):
        self.food_id = data['food_id']
        self.recipe_id = data['recipe_id']
        self.grams = data['grams']
        self.calories = data['calories']
        self.proteins = data['proteins']
        self.carbos = data['carbos']
        self.fats = data['fats']
        self.name = data['name']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO ingredients (food_id, recipe_id, grams, calories, proteins, carbos, fats) values (%(food_id)s, %(recipe_id)s, %(grams)s, %(calories)s, %(proteins)s, %(carbos)s, %(fats)s);'
        return connectToMySQL('xdiet').query_db(query,data)

    @classmethod
    def delete(cls, food_id, recipe_id):
        query = 'DELETE FROM ingredients WHERE food_id = %(food_id)s AND recipe_id = %(recipe_id)s;'
        data = {
            'food_id': food_id,
            'recipe_id': recipe_id
        }
        connectToMySQL('xdiet').query_db(query, data)
    
    @classmethod
    def get_ingredients_by_recipe(cls, id):
        query = 'SELECT * FROM ingredients WHERE recipe_id = %(recipe_id)s;'
        data = {
            'recipe_id' : id
        }
        results = connectToMySQL('xdiet').query_db(query, data)
        ingredients = []
        for ingredient in results:
            ingredient['name'] = food.Food.get_food_by_id(ingredient['food_id']).name
            print(ingredient['name'])
            ingredients.append(cls(ingredient))
        return ingredients

    @classmethod
    def get_ingredients_by_recipe_json(cls, id):
        query = 'SELECT * FROM ingredients WHERE recipe_id = %(recipe_id)s;'
        data = {
            'recipe_id' : id
        }
        results = connectToMySQL('xdiet').query_db(query, data)
        ingredients = []
        for ingredient in results:
            ingredient['name'] = food.Food.get_food_by_id(ingredient['food_id']).name
            ingredients.append(ingredient)
            
        return ingredients

    @staticmethod
    def validate_ingredient(ingredient):
        is_valid = True
        if len(ingredient['grams']) > 0:
            flash('Quantity has to be more than 0', category='ingredient')
            is_valid = False
        return is_valid

    @staticmethod
    def totals_by_recipe(id):
        query = 'SELECT * FROM ingredients WHERE recipe_id = %(recipe_id)s;'
        data = {
            'recipe_id':id
        }
        results = connectToMySQL('xdiet').query_db(query, data)
        totals = {
            'total_calories' : 0,
            'total_proteins' : 0,
            'total_carbos' : 0,
            'total_fats' : 0
        }
        if results != False:
            for ingredient in results:
                totals['total_calories'] += int(ingredient['calories'])
                totals['total_proteins'] += int(ingredient['proteins'])
                totals['total_carbos'] += int(ingredient['carbos'])
                totals['total_fats'] += int(ingredient['fats'])
        return totals

