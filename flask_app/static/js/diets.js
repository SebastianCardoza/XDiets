var dietTable = document.querySelector('#dietTable')
var newDiet = document.querySelector('#newDiet')
var dietMessages = document.querySelector('#dietMessages')
var user_id = 0;
function deleteDiet(id){
    fetch(`/delete_diet/${id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        getDiets()
    })
}
function getDiets(){
    fetch('/get_diets')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        dietTable.innerHTML = ''
        user_id = data.id
        diets = data.diets
        for (let i = 0; i<diets.length; i++){
            var row = document.createElement('tr');
            
            let name = document.createElement('td')
            name.classList.add('mt-4', 'pe-3')
            name.innerHTML = diets[i].name
            row.appendChild(name)
            let type = document.createElement('td')
            type.classList.add('pe-3')
            type.innerHTML = diets[i].type
            row.appendChild(type)
            let actions = document.createElement('td')
            actions.innerHTML = `<a href="/diets/${diets[i].id}">View diet</a>`
            if (user_id == diets[i].user_id){
                actions.innerHTML = `<a href="/diets/${diets[i].id}">View diet</a>
                <span> | </span><a href="/diets/edit/${diets[i].id}">Edit / Add Meals!</a>
                <span> | </span><button onclick="deleteDiet(${diets[i].id})">Delete</button>
                `
            }
            row.appendChild(actions)
            dietTable.appendChild(row)
        }
    })
}
getDiets()
newDiet.onsubmit = function(e) {
    e.preventDefault()
    var form = new FormData(this)
    fetch('process_diet', {method:'POST', body: form})
    .then(response => response.json())
    .then(data => {
        dietMessages.innerHTML = ''
        if ('validated' in data){
            getDiets()
            newDiet.reset()
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