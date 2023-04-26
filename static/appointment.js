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
        }).then(response=>response.text())
        .then(data=>{
            console.log(data);
        });
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

        fetch('/api/check-appointment',
        {
            method: 'POST'
        }).then(response=>response.text())
        .then(data=>{
            console.log(data);
        });
    };
}
if (document.getElementById("logout") !== null) {
    document.getElementById("logout").onclick = function () {
        location.href = "/logout";
    };
}

tutor_list();
async function tutor_list() {
    try {
        const response = await fetch('/api/tutors',
        {
            headers: {
                'Accept': 'application/json'
            }
        })
        const data = await response.json();
        if (response.ok) {
            data.forEach(i => {
                if (i['middle-name']) {
                    appendString = `<tr><td><a href="/tutor?net-id=${i['net-id']}">${i['first-name']} ${i['middle-name']} ${i['last-name']}<br>${i['net-id']}</td>`;
                }
                else {
                    appendString = `<tr><td><a href="/tutor?net-id=${i['net-id']}">${i['first-name']} ${i['last-name']}<br>${i['net-id']}</td>`;
                }
                appendString += `<td>`
                i['subjects'].forEach(j => {
                    appendString += `${j} | `
                })
                appendString += `</td></tr>`;
                $('#tutor-list').append(appendString);
        })
        }
    }catch(e) {
        console.log(e);
    }
}

filter_func();
async function filter_func() {
    try {
        const response = await fetch(`/api/filter?filter=${$('#search').val()}`,
        {
            headers: {
                'Accept': 'application/json'
            }
        })
        const data = await response.json();
        if (response.ok) {
            $('#tutor-table tbody').remove();
            $('#tutor-table').append('<tbody>');
            data.forEach(i => {
                if (i['middle-name']) {
                    appendString = `<tr><td><a href="/tutor?net-id=${i['net-id']}">${i['first-name']} ${i['middle-name']} ${i['last-name']}<br>${i['net-id']}</td>`;
                }
                else {
                    appendString = `<tr><td><a href="/tutor?net-id=${i['net-id']}">${i['first-name']} ${i['last-name']}<br>${i['net-id']}</td>`;
                }
                appendString += `<td>`
                i['subjects'].forEach(j => {
                    appendString += `${j} | `
                })
                appendString += `</td></tr>`;
                $('#tutor-table').append(appendString);
                $('#tutor-table').append('</tbody>');
        })
        }
    }
    catch(e) {
        console.log(e);
    }
    setTimeout(filter_func, 1000)
}

existing_list();
async function existing_list() {
    try {
        const response = await fetch('/api/get-appointments',
        {
            headers: {
                'Accept': 'application/json'
            }
        })
        const data = await response.json();
        console.log(data);
        if (response.ok) {
            data.forEach(i => {
                appendString = `<tr><td>${i[0]} ${i[1]}</td>`
                appendString += `<td>${i[5]} | ${i[4]}</td></tr>`
                $('#appointment-list').append(appendString);
            })
        }
    }
    catch(e) {
        console.log(e);
    }
}