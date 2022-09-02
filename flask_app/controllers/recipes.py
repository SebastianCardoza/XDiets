from flask import redirect, request, render_template, session, flash, jsonify, get_flashed_messages
from flask_app.models import user, recipe, food, ingredient
from flask_app import app

@app.route('/recipes')
def recipes():
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    # recipes = recipe.Recipe.get_all()
    # return render_template('recipes.html', user = user1, recipes = recipes)
    return render_template('recipes.html', user = user1)

@app.route('/recipes/<int:id>')
def the_recipe(id):
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    recipe1 = recipe.Recipe.get_recipe_by_id_with_creator(id)
    ingredients = ingredient.Ingredient.get_ingredients_by_recipe(recipe1.id)
    return render_template('recipe.html', user = user1, recipe = recipe1, ingredients= ingredients)

@app.route('/recipes/edit/<int:id>')
def edit(id):
    if not 'id' in session:
        return redirect('/')
    user1 = user.User.get_user_by_id(session['id'])
    recipe1 = recipe.Recipe.get_recipe_by_id_with_creator(id)
    foods = food.Food.get_all()
    if session['id'] != recipe1.user_id:
        return redirect('/recipes')
    return render_template('edit_recipe.html', user = user1, recipe = recipe1, foods = foods)

@app.route('/get_recipes')
def get_recipes():
    recipes = recipe.Recipe.get_all_json()
    return jsonify(recipes=recipes, id=session['id'])


@app.route('/get_ingredients/<int:recipe_id>')
def get_ingredients(recipe_id):
    ingredients = ingredient.Ingredient.get_ingredients_by_recipe_json(recipe_id)
    return jsonify(ingredients=ingredients, id=session['id'])

@app.route('/get_recipe/<int:id>')
def get_recipe(id):
    recipe1 = recipe.Recipe.get_recipe_by_id_with_creator_json(id)
    return jsonify(recipe1)

@app.route('/delete/<int:id>')
def delete(id):
    if not 'id' in session:
        return redirect('/')
    recipe1 = recipe.Recipe.get_recipe_by_id(id)
    if int(session['id']) == int(recipe1.user_id):
        recipe.Recipe.delete(id)
    return jsonify('')

@app.route('/delete_ing/<int:food_id>/<int:recipe_id>')
def delete_ingredient(food_id, recipe_id):
    if not 'id' in session:
        return redirect('/')
    recipe1 = recipe.Recipe.get_recipe_by_id(recipe_id)
    if int(session['id']) == int(recipe1.user_id):
        ingredient.Ingredient.delete(food_id, recipe_id)
    return jsonify('a ver')