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

