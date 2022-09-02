var diet_name = document.querySelector('#name')
var description = document.querySelector('#description')
var type = document.querySelector('#type')
var mealsDiv = document.querySelector('#meals')
var diet_id = document.querySelector('#diet_id').value
var editdiet = document.querySelector('#editdiet')
var addMeal = document.querySelector('#addMeal')
var dietMessages = document.querySelector('#dietMessages')

function deleteMeal(diet_id, id){
    fetch(`/delete_meal/${diet_id}/${id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        getdiet()
        getMeals()
    })
}
function getdiet(){
    console.log(diet_id)
    fetch(`/get_diet/${diet_id}`)
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        diet_name.innerHTML = data.name
        description.innerHTML = data.description
        type.innerHTML = data.type
    })
}
function getMeals(){
    mealsDiv.innerHTML = ''
    console.log(diet_id)
    fetch(`/get_meals/${diet_id}`)
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        meals = data.meals
        for (let i = 0; i<meals.length; i++){
            let li = document.createElement('li')
            li.classList.add('pb-2')
            li.innerHTML = meals[i].name + ' || Day:' + meals[i].day + ' || ' + meals[i].type + ' || Calories:' + meals[i].total_calories + 
            `<span> | </span><button onclick="deleteMeal(${meals[i].diet_id}, ${meals[i].id})">Delete</buttton>`
            mealsDiv.appendChild(li)
            }
        }
    )
}
getdiet()
getMeals()
editdiet.onsubmit = function(e) {
    e.preventDefault()
    var form = new FormData(this)
    fetch('/process_diet', {method:'POST', body: form})
    .then(response => response.json())
    .then(data => {
        dietMessages.innerHTML = ''
        if ('validated' in data){
            getdiet()
            // editdiet.reset()
        } else {
            console.log(data);
            for (let i = 0; i<data.length; i++){
                let message = document.createElement('p');
                message.innerHTML = data[i]
                message.classList.add('text-danger');
                dietMessages.appendChild(message);
            }
        }
    })
}
addMeal.onsubmit = function(e) {
    e.preventDefault()
    var form = new FormData(this)
    fetch('/process_diet', {method:'POST', body: form})
    .then(response => response.json())
    .then(data => {
        if ('validated' in data){
            getdiet()
            getMeals()
            addMeal.reset()
        } else {
            console.log(data);
        }
    })
}
