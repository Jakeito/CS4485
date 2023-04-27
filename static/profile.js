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
    fetch('/api/check-appointment',
    {
        method: 'POST' 
    });
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

favorite_list();
async function favorite_list() {
    try {
        const response = await fetch('/api/favorite',
        {
            headers: {
                'Accept': 'application/json'
            }
        })
        const data = await response.json();
        if (response.ok) {
            data.forEach(i => {
                if (i['mname']) {
                    appendString = `<tr><td><a href="/tutor?net-id=${i['net-id']}">${i['fname']} ${i['mname']} ${i['lname']} (${i['net-id']})</td></tr>`;
                }
                else {
                    appendString = `<tr><td><a href="/tutor?net-id=${i['net-id']}">${i['fname']} ${i['lname']} (${i['net-id']})</td></tr>`;
                }
                $('#favorite-list').append(appendString);
        })
        }
    }catch(e) {
        console.log(e);
    }
}

info_list();
async function info_list() {
    try {
        let usertype = '';
        fetch('/api/user-type').then(response=>response.text())
        .then(data=>{
            usertype = data;
        })

        const response = await fetch('/api/profile', 
        {
            headers: {
                'Accept': 'application/json'
            }
        })
        const data = await response.json();
        if (response.ok) {
            if (usertype === 'student') {
                if (data['middle-name']) {
                    $('#info').append(`<p1>Name: ${data['first-name']} ${data['middle-name']} ${data['last-name']}</p1><br>`);
                    $('#info').append(`<p1>Net ID: ${data['net-id']}</p1><br>`);
                    $('#info').append(`<p1>Completed Hours: ${data['hours']}</p1><br>`);
                }
                else {
                    $('#info').append(`<p1>Name: ${data['first-name']} ${data['last-name']}</p1><br>`);
                    $('#info').append(`<p1>Net ID: ${data['net-id']}</p1><br>`);
                    $('#info').append(`<p1>Completed Hours: ${data['hours']}</p1><br>`);
                }
            }
            else {
                if (data['middle-name']) {
                    $('#info').append(`<p1>Name: ${data['first-name']} ${data['middle-name']} ${data['last-name']}</p1><br>`);
                    $('#info').append(`<p1>Net ID: ${data['net-id']}</p1><br>`);
                    $('#info').append(`<p1>Completed Hours: ${data['hours']}</p1><br>`);
                    let subjectString = `<p1>Subjects: <br>`;
                    data['subjects'].forEach(i => {
                        subjectString += `${i}<br>`;
                    })
                    subjectString += `</p1><br>`
                    $('#info').append(subjectString);
                    let availabilityString = `<p1>Availability: <br>`;
                    data['availability'].forEach(i => {
                        availabilityString += `${i}<br>`;
                    })
                    availabilityString += `</p1><br>`
                    $('#info').append(availabilityString);
                    $('#info').append(`<p1>About Me: ${data['about-me']}</p1><br>`);
                }
                else {
                    $('#info').append(`<p1>Name: ${data['first-name']} ${data['last-name']}</p1><br>`);
                    $('#info').append(`<p1>Net ID: ${data['net-id']}</p1><br>`);
                    $('#info').append(`<p1>Completed Hours: ${data['hours']}</p1><br>`);
                    let subjectString = `<p1>Subjects: `;
                    data['subjects'].forEach(i => {
                        subjectString += `${i} `;
                    })
                    subjectString += `</p1><br>`
                    $('#info').append(subjectString);
                    let availabilityString = `<p1>Availability: `;
                    data['availability'].forEach(i => {
                        availabilityString += `${i} `;
                    })
                    availabilityString += `</p1><br>`
                    $('#info').append(availabilityString);
                    $('#info').append(`<p1>About Me: ${data['about-me']}</p1><br>`);
                }
            }
        }
    }
    catch(e) {
        console.log(e);
    }
}

get_pic();
async function get_pic() {
    try {
        let id = '';
        fetch('/api/net-id').then(response => response.text())
            .then(data => {
                $('#picture').append(`<img src="/static/tutors/${data}/${data}.png" width="500" height="500">`)
        })
    }
    catch (e) {
        console.log(e);
    }
}