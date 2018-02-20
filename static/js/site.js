const setQuery = require('set-query-string');
const getQuery = require('get-query-param');


let host = window.location.host; // Includes port number.
let protocol = window.location.protocol == 'http:' ? 'ws://' : 'wss://';
let wsUri = protocol + host + '/scan';

let output, button, form, urlField, websocket;

function init() {
    output = document.getElementById("output");
    button = document.getElementById("send");
    form = document.getElementById("url-form");
    urlField = document.getElementById("url");

    form.addEventListener("submit", function (event) {
        submitForm();
        urlField.blur();
        event.preventDefault();
    });

    let url = getQuery('url', window.location.href);
    if (url) {
        urlField.value = url;
        submitForm();
    }
}

function submitForm() {
    setQuery({url: urlField.value.trim()})
    openWebSocket();
}

function openWebSocket() {
    websocket = new WebSocket(wsUri);
    websocket.onopen = function (evt) { onOpen(evt) };
    websocket.onclose = function (evt) { onClose(evt) };
    websocket.onmessage = function (evt) { onMessage(evt) };
    websocket.onerror = function (evt) { onError(evt) };
}

function onOpen(evt) {
    output.innerHTML = '';
    writeToScreen("😻 Scan Cat woke up.");
    checkForURLAndAutoSubmit();
}

function onClose(evt) {
    writeToScreen("😽 Scan Cat sleeps now.");
}

function onMessage(evt) {
    writeToScreen('<span class="message">' + evt.data + '</span>');
}

function onError(evt) {
    writeToScreen('<span class="error">ERROR:</span> ' + evt.data);
}

function doSend(message) {
    websocket.send(message);
}

function writeToScreen(message) {
    let pre = document.createElement("p");
    pre.style.wordWrap = "break-word";
    pre.innerHTML = message;
    output.appendChild(pre);
}

function checkForURLAndAutoSubmit() {
    let url = getQuery('url', window.location.href);
    if (url) {
        doSend(url.trim());
    }
}

window.addEventListener("load", init, false);
