(function () {
    var host = window.location.host; // Includes port number.
    var protocol = window.location.protocol == 'http:' ? 'ws://' : 'wss://';
    var wsUri = protocol + host + '/scan';

    var output, button, form, urlField;

    function init() {
        output = document.getElementById("output");
        button = document.getElementById("send");
        form = document.getElementById("url-form");
        urlField = document.getElementById("url");

        openWebSocket();

        form.addEventListener("submit", function (event) {
            output.innerHTML = '';
            doSend(urlField.value.trim());
            event.preventDefault();
            urlField.value = '';
        });
    }

    function openWebSocket() {
        websocket = new WebSocket(wsUri);
        websocket.onopen = function (evt) { onOpen(evt) };
        websocket.onclose = function (evt) { onClose(evt) };
        websocket.onmessage = function (evt) { onMessage(evt) };
        websocket.onerror = function (evt) { onError(evt) };
    }

    function onOpen(evt) {
        writeToScreen("😻 Scan Cat is connected.");
        checkForURLAndAutoSubmit();
    }

    function onClose(evt) {
        writeToScreen("🙀 Disconnected. Please <a href='/'>refresh</a>.");
    }

    function onMessage(evt) {
        writeToScreen('<span class="message">' + evt.data + '</span>');
        // websocket.close();
    }

    function onError(evt) {
        writeToScreen('<span class="error">ERROR:</span> ' + evt.data);
    }

    function doSend(message) {
        // writeToScreen("SENT: " + message);
        websocket.send(message);
    }

    function writeToScreen(message) {
        var pre = document.createElement("p");
        pre.style.wordWrap = "break-word";
        pre.innerHTML = message;
        output.appendChild(pre);
    }

    function checkForURLAndAutoSubmit() {
        var urlParams = new URLSearchParams(window.location.search);
        var requestedUrl = urlParams.get('url');
        if (requestedUrl) {
            doSend(requestedUrl);
        }
    }

    window.addEventListener("load", init, false);
})();
