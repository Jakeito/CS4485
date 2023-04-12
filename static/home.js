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
        location.href = "/profile/";
    };
}
if (document.getElementById("logout") !== null) {
    document.getElementById("logout").onclick = function () {
        location.href = "/logout";
    };
}