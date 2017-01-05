var ws = new WebSocket("ws://127.0.0.1:8080/websocket");

ws.onopen = function() {
   ws.send("Hello, world");
};

ws.onmessage = function (evt) {
   alert(evt.data);
};