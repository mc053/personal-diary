function login() {
    window.location.pathname = "/login";
}

function create() {
    window.location.pathname = "/create";
}

function home() {
    window.location.pathname = "/";
}

function addText() {
    window.location.pathname = "/add/text"
}

function addPicture() {
    window.location.pathname = "/add/picture"
}

function deleteText(index) {
    window.location.pathname = "/delete/text/" + index
}

function deletePicture(index) {
    window.location.pathname = "/delete/picture/" + index
}

function editText(index) {
    window.location.pathname = "/edit/text/" + index
}

function editPicture(index) {
    window.location.pathname = "/edit/picture/" + index
}