var recipe_name = document.querySelector('#name')
var description = document.querySelector('#description')
var recipe_img = document.querySelector('#recipe_img')
var instructions = document.querySelector('#instructions')
var ingredientsDiv = document.querySelector('#ingredients')
var total_calories = document.querySelector('#total_calories')
var recipe_id = document.querySelector('#recipe_id').value
var editRecipe = document.querySelector('#editRecipe')
var addIngredient = document.querySelector('#addIngredient')
var recipeMessages = document.querySelector('#recipeMessages')

function deleteIngredient(food_id, recipe_id){
    fetch(`/delete_ing/${food_id}/${recipe_id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        getRecipe()
        getIngredients()
    })
}
function getRecipe(){
    console.log(recipe_id)
    fetch(`/get_recipe/${recipe_id}`)
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        recipe_name.innerHTML = data.name
        description.innerHTML = data.description
        instructions.innerHTML = data.instructions
        total_calories.innerHTML = data.total_calories
        total_proteins.innerHTML = data.total_proteins
        total_carbos.innerHTML = data.total_carbos
        total_fats.innerHTML = data.total_fats
        recipe_img.src = data.img_url
    })
}
function getIngredients(){
    ingredientsDiv.innerHTML = ''
    console.log(recipe_id)
    fetch(`/get_ingredients/${recipe_id}`)
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        ingredients = data.ingredients
        for (let i = 0; i<ingredients.length; i++){

            let li = document.createElement('li')
            li.classList.add('pb-2')
            li.innerHTML = ingredients[i].name + ' || Grams:' + ingredients[i].grams + ' || Calories:' + ingredients[i].calories + 
            `<span> | </span><button onclick="deleteIngredient(${ingredients[i].food_id}, ${ingredients[i].recipe_id})">Delete</buttton>`
            // let actions = document.createElement('td')
            // actions.innerHTML = `<a href="/ingredients/edit/${ingredients[i].id}">Edit / Add Ingredients!</a>
            // <span> | </span><a onclick="deleteRecipe(${ingredients[i].id})">Delete</a>`
            // if (user_id == ingredients[i].user_id){
            //     actions.innerHTML = `<a href="/ingredients/${ingredients[i].id}">View Recipe</a>
            //     <span> | </span><a href="/ingredients/edit/${ingredients[i].id}">Edit</a>
            //     <span> | </span><a onclick="deleteRecipe(${ingredients[i].id})">Delete</a>
            //     `
            // // }
            // row.appendChild(actions)
            ingredientsDiv.appendChild(li)
        }
    })
}
getRecipe()
getIngredients()
editRecipe.onsubmit = function(e) {
    e.preventDefault()
    var form = new FormData(this)
    fetch('/process', {method:'POST', body: form})
    .then(response => response.json())
    .then(data => {
        recipeMessages.innerHTML = ''
        if ('validated' in data){
            getRecipe()
            editRecipe.reset()
        } else {
            console.log(data);
            for (let i = 0; i<data.length; i++){
                let message = document.createElement('p');
                message.innerHTML = data[i]
                message.classList.add('text-danger');
                recipeMessages.appendChild(message);
            }
        }
    })
}
addIngredient.onsubmit = function(e) {
    e.preventDefault()
    var form = new FormData(this)
    fetch('/process', {method:'POST', body: form})
    .then(response => response.json())
    .then(data => {
        if ('validated' in data){
            getRecipe()
            getIngredients()
            addIngredient.reset()
        } else {
            console.log(data);
        }
    })
}
