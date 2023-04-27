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

var meet = flatpickr('input[type=datetime-local]', {
    enableTime: true,
    minDate: 'today',
    time_24hr: true,

});

if (document.getElementById("submit") !== null) {
    document.getElementById("submit").onclick = function () {
        const date = meet.latestSelectedDateObj.toString();
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const id = urlParams.get('net-id');

        fetch(`/api/register-appointment?net-id=${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'date': date
            })
        }).then(response=>response.text())
        .then(data=>{
            if (data !== 'Success') {
                alert(data);
            }
            else {
                window.location.href = '/appointment';
            }
        });
    }
}

