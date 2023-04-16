document.getElementById("home").onclick = function () {
    location.href = "/home";
};
document.getElementById("about").onclick = function () {
    location.href = "/about";
};
document.getElementById("suppSubj").onclick = function () {
    location.href = "/suppSubj";
};
if (document.getElementById("requestAppointment") !== null) {
    document.getElementById("requestAppointment").onclick = function () {
        location.href = "/appointment";
    };
}
if (document.getElementById("signin") !== null) {
    document.getElementById("signin").onclick = function () {
        location.href = "/signin";
    };
}
if (document.getElementById("profile") !== null ) {
    document.getElementById("profile").onclick = function () {
        fetch('/api/net-id').then(response=>response.text())
        .then(data=>{
            location.href = "/profile/" + data;
        })
    };
}
if (document.getElementById("logout") !== null) {
    document.getElementById("logout").onclick = function () {
        location.href = "/logout";
    };
}
document.getElementById("signup-student").onclick = function () {
    location.href = "/register-student";
}
$(document).ready(function () {
    $('#signup').click(register_tutor);
})

function register_tutor() {
    var firstName = $('#input-first-name').val();
    var middleName = $('#input-middle-name').val();
    var lastName = $('#input-last-name').val();
    var netID = $('#input-net-id').val();
    var password = $('#input-password').val();
    var aboutMe = $('#tutor-about-me').val();
    var picture = document.querySelector('input[type="file"]')
    var supportSubjects = $('#tutor-supported-subjects').val();
    var availability = $('#tutor-availability').val();
    var pictureFile = new FormData();
    pictureFile.append('file', picture.files[0]);

    console.log(netID + '\n' + password)
    if (firstName !== '' && lastName !== '' && netID !== '' && password !== '' && aboutMe !== '' && supportSubjects !== '' && availability !== ''){
        fetch('/api/register-tutor', {
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
                'about-me': aboutMe,
                'support-subjects': supportSubjects,
                'availability': availability,
                'user-type': 'tutor'
            })
        }).then(response=>response.text())
        .then(data=>{
            if (data !== 'Valid') {
                alert(data);
            }
            else {
                window.location.href = '/home';
            }
        });

        fetch('/api/tutor-picture?net-id=${netID}', {
            method: 'POST',
            body: pictureFile
        }).then(response=>response.text())
        .then(data=>{
            if (data !== 'Valid') {
                alert(data);
            }
            else {
                window.location.href = '/home';
            }
        });
    }
}