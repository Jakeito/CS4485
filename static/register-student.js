document.getElementById("home").onclick = function () {
    location.href = "/home";
};
document.getElementById("about").onclick = function () {
    location.href = "/about";
};
document.getElementById("suppSubj").onclick = function () {
    location.href = "/subjects";
};
if (document.getElementById("requestAppointment") !== null) {
    document.getElementById("requestAppointment").onclick = function () {
        location.href = "/appointment";

        fetch('/api/check-appointment',
            {
                method: 'POST'
            });
    };
}
if (document.getElementById("signin") !== null) {
    document.getElementById("signin").onclick = function () {
        location.href = "/signin";
    };
}
if (document.getElementById("profile") !== null) {
    document.getElementById("profile").onclick = function () {
        fetch('/api/net-id').then(response => response.text())
            .then(data => {
                location.href = "/profile/" + data;
            })

        fetch('/api/check-appointment',
            {
                method: 'POST'
            });
    };
}
if (document.getElementById("logout") !== null) {
    document.getElementById("logout").onclick = function () {
        location.href = "/logout";
    };
}
document.getElementById("signup-tutor").onclick = function () {
    location.href = "/register-tutor";
}

document.getElementById('signup').addEventListener('click', function(e) {
    e.preventDefault();
    register_student();
})

function register_student() {
    var firstName = $('#input-first-name').val()
    var middleName = $('#input-middle-name').val()
    var lastName = $('#input-last-name').val()
    var netID = $('#input-net-id').val()
    var password = $('#input-password').val()
    if (firstName !== '' && lastName !== '' && netID !== '' && password !== ''){
        fetch('/api/register-student', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'first-name': firstName,
                'middle-name': middleName,
                'last-name': lastName,
                'net-id': netID,
                'password': password,
                'user-type': 'student'
            })
        }).then(response=>response.text())
        .then(data=>{
            if (data !== 'Valid') {
                alert(data);
            }
            else {
                location.href = '/home';
            }
        });
    }
}