document.getElementById("home").onclick = function () {
    location.href = "/home";
};
document.getElementById("about").onclick = function () {
    location.href = "/about";
};
document.getElementById("suppSubj").onclick = function () {
    location.href = "/suppSubj";
};
document.getElementById("signin").onclick = function () {
    location.href = "/signin";
};
document.getElementById("signup-tutor").onclick = function () {
    location.href = "/register-tutor";
}
$(document).ready(function () {
    $('#signup').click(register_student)
})


function register_student() {
    const firstName = $('#input-first-name').val()
    const middleName = $('#input-middle-name').val()
    const lastName = $('#input-last-name').val()
    const netID = $('#input-net-id').val()
    const password = $('#input-password').val()
    console.log(netID + '\n' + password)
    const response = fetch('/api/register-student', {
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
    })

    //If response is not success, send error message to user
}