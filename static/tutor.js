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
document.getElementById("request").onclick = function () {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const id = urlParams.get('net-id');
    location.href = `/booking?net-id=${id}`;
};

if (document.getElementById("favorite") !== null) {
    document.getElementById("favorite").onclick = function () {
        check_favorite('modify');
    };
}

check_favorite('check');
async function check_favorite(mode) {
    try {
        $('#fav').remove();
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const id = urlParams.get('net-id');

        const response = await fetch(`/api/check-favorite?net-id=${id}`,
        {
            headers: {
                'Accept': 'application/json'
            }
        })
        const data = await response.text();

        if (data === 'false') {
            $('#favorite').append(`<i id="fav" class="bi- bi-star" style="font-size: xx-large;"></i>`);
            if (mode === 'modify') {
                fetch('/api/add-favorite-tutor', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'tutor-id': id
                    })
                })
                $('#fav').remove();
                $('#favorite').append(`<i id="fav" class="bi- bi-star-fill" style="font-size: xx-large; color: yellow;"></i>`)
            }
        }
        else {
            $('#favorite').append(`<i id="fav" class="bi- bi-star-fill" style="font-size: xx-large; color: yellow;"></i>`)
            if (mode === 'modify') {
                fetch('/api/remove-favorite-tutor', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'tutor-id': id
                    })
                })
                $('#fav').remove();
                $('#favorite').append(`<i id="fav" class="bi- bi-star" style="font-size: xx-large;"></i>`);
            }
        }
    }
    catch(e) {
        console.log(e);
    }
}

info_list();
async function info_list() {
    try {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const id = urlParams.get('net-id');

        const response = await fetch(`/api/tutor?net-id=${id}`,
            {
                headers: {
                    'Accept': 'application/json'
                }
            })
        const data = await response.json();
        if (response.ok) {
            if (data['middle-name']) {
                $('#tutor-info').append(`<p1>Name: ${data['first-name']} ${data['middle-name']} ${data['last-name']}</p1><br>`);
                $('#tutor-info').append(`<p1>Net ID: ${data['net-id']}</p1><br>`);
                $('#tutor-info').append(`<p1>Completed Hours: ${data['hours']}</p1><br>`);
                let subjectString = `<p1>Subjects: <br>`;
                data['subjects'].forEach(i => {
                    subjectString += `${i}<br>`;
                })
                subjectString += `</p1><br>`
                $('#tutor-info').append(subjectString);
                let availabilityString = `<p1>Availability: <br>`;
                data['availability'].forEach(i => {
                    availabilityString += `${i}<br>`;
                })
                availabilityString += `</p1><br>`
                $('#tutor-info').append(availabilityString);
                $('#tutor-info').append(`<p1>About Me: ${data['about-me']}</p1><br>`);
            }
            else {
                $('#tutor-info').append(`<p1>Name: ${data['first-name']} ${data['last-name']}</p1><br>`);
                $('#tutor-info').append(`<p1>Net ID: ${data['net-id']}</p1><br>`);
                $('#tutor-info').append(`<p1>Completed Hours: ${data['hours']}</p1><br>`);
                let subjectString = `<p1>Subjects: `;
                data['subjects'].forEach(i => {
                    subjectString += `${i} `;
                })
                subjectString += `</p1><br>`
                $('#tutor-info').append(subjectString);
                let availabilityString = `<p1>Availability: `;
                data['availability'].forEach(i => {
                    availabilityString += `${i} `;
                })
                availabilityString += `</p1><br>`
                $('#tutor-info').append(availabilityString);
                $('#tutor-info').append(`<p1>About Me: ${data['about-me']}</p1><br>`);
            }
        }
    }
    catch (e) {
        console.log(e);
    }
}

get_pic();
async function get_pic() {
    try {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const id = urlParams.get('net-id');

        $('#picture').append(`<img src="/static/tutors/${id}/${id}.png" width="500" height="500">`)
    }
    catch (e) {
        console.log(e);
    }
}