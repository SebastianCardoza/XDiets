from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import recipe
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []
        self.diets = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (name, email, password) values (%(name)s, %(email)s, %(password)s);'
        return connectToMySQL('xdiet').query_db(query,data)

    @classmethod
    def get_user_by_id_with_recipes(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('xdiet').query_db(query, data)
        user = cls(results[0])
        user.recipes = recipe.Recipe.get_recipe_by_id(id)
        return user

    @classmethod
    def get_user_by_id(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        data = {'id':id}
        results = connectToMySQL('xdiet').query_db(query, data)
        user = cls(results[0])
        return user

    @classmethod
    def get_user_by_email(cls, email):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {'email': email}
        results = connectToMySQL('xdiet').query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL('xdiet').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        data = {'id': id}
        connectToMySQL('xdiet').query_db(query, data)

    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['name']) < 2:
            flash('Name has to be at least 2 characters', category='register')
            is_valid = False
        if User.get_user_by_email(user['email']) != False:
            flash('Email already exists', category='register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Email is not valid', category='register')    
            is_valid = False
        if len(user['password']) < 8:
            flash('Password has to be at least 8 characters', category='register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords doesnt match', category='register')
            is_valid = False
        return is_valid
