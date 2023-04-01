document.getElementById("home").onclick = function () {
    location.href = "/home";
};
document.getElementById("about").onclick = function () {
    location.href = "/about";
};
document.getElementById("suppSubj").onclick = function () {
    location.href = "/suppSubj";
};
if (document.getElementById("signin") !== null) {
    document.getElementById("signin").onclick = function () {
        location.href = "/signin";
    };
}
if (document.getElementById("profile") !== null ) {
    document.getElementById("profile").onclick = function () {
        location.href = "/profile/";
    };
}
if (document.getElementById("logout") !== null) {
    document.getElementById("logout").onclick = function () {
        location.href = "/logout";
    };
}
document.getElementById("signup").onclick = function () {
    location.href = "/register-student"
}

$(document).ready(function () {
    $('#signin-button').click(signin);
})

function signin() {
    const netID = $('#input-net-id').val();
    const password = $('#input-password').val();
    console.log(netID + '\n' + password)
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'net-id': netID,
            'password': password
        })
    }).then(response=>response.text())
    .then(data=>{
        if (data === 'Invalid username or password') {
            alert('Invalid username or password! Try again!');
        }
        else {
            window.location.href = '/home';
        }
    });
}