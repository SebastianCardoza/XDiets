var registerForm = document.querySelector('#registerForm');
var loginForm = document.querySelector('#loginForm');
var register_messages = document.querySelector('#register_messages');
var login_messages = document.querySelector('#login_messages');

registerForm.onsubmit = function(e) {
    e.preventDefault();
    form = new FormData(this)
    fetch('/process', {method: 'POST', body: form, redirect: 'follow'})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        login_messages.innerHTML = '';
        register_messages.innerHTML = '';
        if ('url' in data) {
            window.location.href = '/diets';
        } else {
            for(let i=0; i<data.length; i++ ){
                let message = document.createElement('p');
                message.classList.add('text-danger');
                message.innerText = data[i];
                register_messages.appendChild(message);
            }
        }
    })
}
loginForm.onsubmit = function(e) {
    e.preventDefault();
    form = new FormData(this)
    fetch('/process', {method: 'POST', body: form, redirect: 'follow'})
    .then(response => response.json())
    .then(data => {
        console.log(data);
        login_messages.innerHTML = '';
        register_messages.innerHTML = '';
        if ('url' in data) {
            window.location.href = '/diets';
        } else {
            for(let i=0; i<data.length; i++ ){
                let message = document.createElement('p');
                message.classList.add('text-danger');
                message.innerText = data[i];
                login_messages.appendChild(message);
            }
        }
    })
}