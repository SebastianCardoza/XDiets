from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import recipe
from flask import flash

class Food:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.calories = data['calories']
        self.proteins = data['proteins']
        self.carbos = data['carbos'] 
        self.fats = data['fats']

    @classmethod
    def get_food_by_id(cls, id):
        query = 'SELECT * FROM foods WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('xdiet').query_db(query, data)
        food = cls(results[0])
        return food

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM foods;'
        results = connectToMySQL('xdiet').query_db(query)
        foods = []
        for food in results:
            foods.append(cls(food))
        return foods














    # EXTRA COMMANDS

    # @classmethod
    # def get_user_by_id_with_foods(cls, id):
    #     query = 'SELECT * FROM foods WHERE id = %(id)s;'
    #     data = {'id':id}
    #     results = connectToMySQL('xdiet').query_db(query, data)
    #     user = cls(results[0])
    #     user.foods = recipe.Recipe.get_recipe_by_id(id)
    #     return user

    # @staticmethod
    # def validate_register(user):
    #     is_valid = True
    #     if len(user['name']) < 2:
    #         flash('Name has to be at least 2 characters', category='register')
    #         is_valid = False
    #     if User.get_user_by_email(user['email']) != False:
    #         flash('Email already exists', category='register')
    #         is_valid = False
    #     if not EMAIL_REGEX.match(user['email']):
    #         flash('Email is not valid', category='register')    
    #         is_valid = False
    #     if len(user['password']) < 8:
    #         flash('Password has to be at least 8 characters', category='register')
    #         is_valid = False
    #     if user['password'] != user['confirm_password']:
    #         flash('Passwords doesnt match', category='register')
    #         is_valid = False
    #     return is_valid

    # @classmethod
    # def delete(cls, id):
    #     query = 'DELETE FROM foods WHERE id = %(id)s;'
    #     data = {'id': id}
    #     connectToMySQL('xdiet').query_db(query, data)