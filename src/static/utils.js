function login() {
    window.location.pathname = "/login";
}

function logout() {
    window.location.pathname = "/logout";
}

function create() {
    window.location.pathname = "/create";
}

function home() {
    window.location.pathname = "/";
}

function diary() {
    window.location.pathname = "/diary";
}

function addText() {
    window.location.pathname = "/add/text"
}

function addPicture() {
    window.location.pathname = "/add/picture"
}

function deleteText(index) {
    if (confirm("Do you really want to delete this text?")) {
        window.location.pathname = "/delete/text/" + index
    }
}

function deletePicture(index) {
    if (confirm("Do you really want to delete this picture?")) {
        window.location.pathname = "/delete/picture/" + index
    }
}

function editText(index) {
    window.location.pathname = "/edit/text/" + index
}

function editPicture(index) {
    window.location.pathname = "/edit/picture/" + index
}