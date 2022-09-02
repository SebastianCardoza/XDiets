from operator import truediv
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import recipe
from flask import flash
from flask_app.models import user, meal, recipe

class Diet:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name'] 
        self.description = data['description'] 
        self.type = data['type'] 
        self.user_id = data['user_id'] 
        self.meals = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO diets (name, description, type, user_id) values (%(name)s, %(description)s, %(type)s, %(user_id)s);'
        return connectToMySQL('xdiet').query_db(query,data)

    @classmethod
    def get_diet_by_id(cls, id):
        query = 'SELECT * FROM diets WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('xdiet').query_db(query, data)
        diet = cls(results[0])
        return diet

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM diets;'
        results = connectToMySQL('xdiet').query_db(query)
        diets = []
        for diet in results:
            diets.append(cls(diet))
        return diets

    @classmethod
    def update(cls, data):
        query = 'UPDATE diets SET name = %(name)s, description = %(description)s, type = %(type)s WHERE id = %(diet_id)s;'    
        connectToMySQL('xdiet').query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM diets WHERE id = %(id)s;'
        data = {'id': id}
        connectToMySQL('xdiet').query_db(query, data)

    @classmethod
    def get_diet_by_id_json(cls, id):
        query = 'SELECT * FROM diets WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('xdiet').query_db(query, data)
        diet = results[0]
        diet['creator_name'] = user.User.get_user_by_id(diet['user_id']).name
        return diet

    @classmethod
    def get_all_json(cls):
        query = 'SELECT * FROM diets;'
        results = connectToMySQL('xdiet').query_db(query)
        diets = []
        for diet in results:
            diet['creator_name'] = user.User.get_user_by_id(diet['user_id']).name
            print(diet['id'] , 'que fueeee')
            meals = meal.Meal.get_meals_by_diet(diet['id'])
            try:
                diet['img_url'] = recipe.Recipe.get_recipe_by_id(meals[0].recipe_id).img_url
            except IndexError: 
                diet['img_url'] = 'https://cdn.dribbble.com/users/2460221/screenshots/8429684/media/225b2f10d124b2024b90a8e2348a78ee.jpg'
            diets.append(diet)
        return diets

    @staticmethod
    def validate(diet):
        is_valid = True
        if len(diet['name']) < 3:
            flash('Name has to be at least 3 characters', category='new_diet')
            is_valid = False
        if len(diet['description']) < 3:
            flash('Description has to be at least 3 characters', category='new_diet')
            is_valid = False
        if len(diet['dtype']) < 2:
            flash('Type have to be at least 2 characters', category='new_diet')
            is_valid = False
        return is_valid