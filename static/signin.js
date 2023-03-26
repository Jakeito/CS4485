document.getElementById('home').onclick = function () {
    location.href = '/home';
};
document.getElementById('about').onclick = function () {
    location.href = '/about';
};
document.getElementById('suppSubj').onclick = function () {
    location.href = '/suppSubj';
};
document.getElementById('signin').onclick = function () {
    location.href = '/signin';
};
document.getElementById('signup').onclick = function () {
    location.href = '/register-student';
};
document.getElementById('profile').onclick = function () {
    location.href = '/profile/';
};
document.getElementById('logout').onclick = function () {
    location.href = '/logout';
};

$(document).ready(function () {
    $('#signin-button').click(signin)
})

function signin() {
    const netID = $('#input-net-id').val()
    const password = $('#input-password').val()
    console.log(netID + '\n' + password)
    const response = fetch('/api/signin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'net-id': netID,
            'password': password
        })
    })
}