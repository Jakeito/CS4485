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

if (document.getElementById("submit") !== null) {
    document.getElementById("submit").onclick = function () {
        const dateTime = flatpickr(document.getElementById("meeting-date-time"), {"enableTime":true});
        console.log(dateTime.selectedDates)
        console.log(dateTime.latestSelectedDateObj)
        console.log(dateTime.latestSelectedDateObj.getUTCFullYear())
        console.log(dateTime.latestSelectedDateObj.getUTCMonth())
        console.log(dateTime.latestSelectedDateObj.getDate())
        console.log(dateTime.latestSelectedDateObj.getHours())
        console.log(dateTime.latestSelectedDateObj.getMinutes())
        console.log(dateTime.latestSelectedDateObj.toJSON())
        console.log(dateTime.latestSelectedDateObj.toDateString())
        console.log(dateTime.latestSelectedDateObj.toTimeString())
        console.log(dateTime.latestSelectedDateObj.toUTCString())
        console.log(dateTime.latestSelectedDateObj.toString())
        console.log(dateTime)
    };
}

