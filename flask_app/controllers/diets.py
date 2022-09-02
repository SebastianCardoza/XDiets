from flask import redirect, request, render_template, session, flash, jsonify, get_flashed_messages
from flask_app.models import user, recipe, food, ingredient, diet, meal
from flask_app import app

@app.route('/diets')
def diets():
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    return render_template('diets.html', user = user1)

@app.route('/process_diet', methods = ['POST'])
def process_diet():
    if not 'id' in session:
        return redirect('/')
    if request.form['type'] == 'new_diet':
        if not diet.Diet.validate(request.form):
                return jsonify(get_flashed_messages(category_filter=['new_diet']))
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'type': request.form['dtype'],
            'user_id': request.form['user_id']
        }
        diet.Diet.save(data)   
        return jsonify(validated='true')
    # Update edit or send flash messages
    elif request.form['type'] == 'edit_diet':
        if not diet.Diet.validate(request.form):
            return jsonify(get_flashed_messages(category_filter=['new_diet']))
        data = {
            'diet_id': request.form['diet_id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'type': request.form['dtype']
        }
        diet.Diet.update(data)
        return jsonify(validated='true')
    elif request.form['type'] == 'add_meal':
        data = {
            'diet_id': request.form['diet_id'],
            'recipe_id': request.form['recipe_id'],
            'time': request.form['time'],
            'type': request.form['mtype'],
            'day': request.form['day']
        }
        print(data)
        meal.Meal.save(data)
        return jsonify(validated='true')  

@app.route('/diets/edit/<int:id>')
def edit_diet(id):
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    diet1 = diet.Diet.get_diet_by_id(id)
    recipes = recipe.Recipe.get_all()
    if session['id'] != diet1.user_id:
        return redirect('/diets')
    return render_template('edit_diet.html', user = user1, diet = diet1, recipes = recipes)

@app.route('/diets/<int:id>')
def the_diet(id):
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    diet1 = diet.Diet.get_diet_by_id(id)
    meals = meal.Meal.get_meals_by_diet(diet1.id)
    return render_template('diet.html', user = user1, diet = diet1, meals= meals)


@app.route('/get_diets')
def get_diets():
    diets = diet.Diet.get_all_json()
    return jsonify(diets=diets)

@app.route('/get_diet/<int:id>')
def get_diet(id):
    diet1 = diet.Diet.get_diet_by_id_json(id)
    return jsonify(diet1)

@app.route('/get_meals/<int:diet_id>')
def get_meals(diet_id):
    meals = meal.Meal.get_meals_by_diet_json(diet_id)
    return jsonify(meals=meals, id=session['id'])

@app.route('/delete_diet/<int:id>')
def delete_diet(id):
    if not 'id' in session:
        return redirect('/')
    diet1 = diet.Diet.get_diet_by_id(id)
    if int(session['id']) == int(diet1.user_id):
        diet.Diet.delete(id)
    return jsonify('')

@app.route('/delete_meal/<int:diet_id>/<int:meal_id>')
def delete_meal(diet_id, meal_id):
    if not 'id' in session:
        return redirect('/')
    diet1 = diet.Diet.get_diet_by_id(diet_id)
    if int(session['id']) == int(diet1.user_id):
        meal.Meal.delete(diet_id, meal_id)
    return jsonify('a ver')