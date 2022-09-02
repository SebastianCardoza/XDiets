from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import diet, recipe, ingredient
from flask import flash

class Meal:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.diet_id = data['diet_id']
        self.recipe_id = data['recipe_id']
        self.type = data['type']
        self.time = data['day']
        self.time = data['time']
        self.total_calories = data['total_calories']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO meals (diet_id, recipe_id, type, time, day) values (%(diet_id)s, %(recipe_id)s, %(type)s, %(time)s, %(day)s);'
        return connectToMySQL('xdiet').query_db(query,data)

    @classmethod
    def delete(cls, diet_id, meal_id):
        query = 'DELETE FROM meals WHERE diet_id = %(diet_id)s AND id = %(meal_id)s;'
        data = {
            'diet_id': diet_id,
            'meal_id': meal_id
        }
        connectToMySQL('xdiet').query_db(query, data)
    
    @classmethod
    def get_meals_by_diet(cls, id):
        query = 'SELECT * FROM meals WHERE diet_id = %(diet_id)s ORDER BY meals.day, meals.time ;'
        data = {
            'diet_id' : id
        }
        results = connectToMySQL('xdiet').query_db(query, data)
        meals = []
        for meal in results:
            meal['total_calories'] = ingredient.Ingredient.totals_by_recipe(meal['recipe_id'])['total_calories']
            meal['name'] = recipe.Recipe.get_recipe_by_id(meal['recipe_id']).name
            print(meal['name'])
            meals.append(cls(meal))
        return meals

    @classmethod
    def get_meals_by_diet_json(cls, id):
        query = 'SELECT * FROM meals WHERE meals.diet_id = %(diet_id)s ORDER BY meals.day, meals.time;'
        data = {
            'diet_id' : id
        }
        results = connectToMySQL('xdiet').query_db(query, data)
        meals = []
        for meal in results:
            meal['name'] = recipe.Recipe.get_recipe_by_id(meal['recipe_id']).name
            meal['total_calories'] = ingredient.Ingredient.totals_by_recipe(meal['recipe_id'])['total_calories']
            meal['total_proteins'] = ingredient.Ingredient.totals_by_recipe(meal['recipe_id'])['total_proteins']
            meal['total_carbos'] = ingredient.Ingredient.totals_by_recipe(meal['recipe_id'])['total_carbos']
            meal['total_fats'] = ingredient.Ingredient.totals_by_recipe(meal['recipe_id'])['total_fats']
            meals.append(meal)
        return meals

    @staticmethod
    def validate_meal(meal):
        is_valid = True
        if len(meal['grams']) > 0:
            flash('Quantity has to be more than 0', category='meal')
            is_valid = False
        return is_valid