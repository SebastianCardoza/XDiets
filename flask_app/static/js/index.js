dietDiv = document.querySelector('#dietDiv')
getDiets()
function getDiets(){
    fetch('/get_diets')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        dietDiv.innerHTML = ''
        user_id = data.id
        diets = data.diets
        for (let i = 0; i<diets.length; i++){
            var card = document.createElement('div');
            card.classList.add('card', 'p-0', 'm-2')
            card.style.width = '18rem'
            card.innerHTML = `
            <img class="card-img-top" src="${diets[i].img_url}"alt="Card image cap">
            <div class="card-body">
                <h5 class="card-title">${diets[i].name}</h5>
                <p class="card-text">${diets[i].description}</p>
                <a href="/diets/${diets[i].id}" class="btn btn-primary">See Diet</a>
            </div>`
            
            dietDiv.appendChild(card)
        }
    })
}