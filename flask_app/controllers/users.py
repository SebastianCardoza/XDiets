from flask import redirect, request, render_template, session, flash, jsonify, get_flashed_messages
from flask_app.models import user, recipe, food, ingredient, diet
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.controllers import recipes, diets

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    if 'id' in session:
        return redirect('/diets')
    return render_template('register.html')

@app.route('/process', methods = ['POST'])
def process():
    if request.form['type'] == 'register':
        if not user.User.validate_register(request.form):
            return jsonify(get_flashed_messages(category_filter=['register']))
        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'password':bcrypt.generate_password_hash(request.form['password']) 
        }
        session['id'] = user.User.save(data)
        return jsonify(url='/diets')

    elif request.form['type'] == 'login':
        user1 = user.User.get_user_by_email(request.form['email']) 
        if user1 == False or not bcrypt.check_password_hash(user1.password, request.form['password']):
            flash('Invalid email/password', category = 'login')
            return jsonify(get_flashed_messages(category_filter=['login']))
        session['id'] = user1.id
        session['name'] = user1.name
        print(session['name'])
        return jsonify(url='/diets')
    elif request.form['type'] == 'new_recipe':
        if not recipe.Recipe.validate_recipe(request.form):
            return jsonify(get_flashed_messages(category_filter=['new_recipe']))
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'img_url': request.form['img_url'],
            'user_id': request.form['user_id']
        }
        id = recipe.Recipe.save(data)   
        return jsonify(validated='true')
    elif request.form['type'] == 'edit_recipe':
        if not recipe.Recipe.validate_recipe(request.form):
            return jsonify(get_flashed_messages(category_filter=['new_recipe']))
        data = {
            'recipe_id': request.form['recipe_id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'img_url': request.form['img_url']
        }
        recipe.Recipe.update(data)
        return jsonify(validated='true') 
    elif request.form['type'] == 'add_ingredient':
        calories = int(food.Food.get_food_by_id(request.form['food_id']).calories) * int(request.form['grams']) / 100
        proteins = int(food.Food.get_food_by_id(request.form['food_id']).proteins) * int(request.form['grams']) / 100
        carbos = int(food.Food.get_food_by_id(request.form['food_id']).carbos) * int(request.form['grams']) / 100
        fats = int(food.Food.get_food_by_id(request.form['food_id']).fats) * int(request.form['grams']) / 100
        print(calories)
        data = {
            'recipe_id': request.form['recipe_id'],
            'food_id': request.form['food_id'],
            'grams': request.form['grams'],
            'calories': calories,
            'proteins': proteins,
            'carbos': carbos,
            'fats': fats
        }
        print(data)
        ingredient.Ingredient.save(data)
        return jsonify(validated='true') 

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')