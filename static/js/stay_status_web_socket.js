var WS_URL = "ws://localhost:8888/ws/"

var ws = new WebSocket(WS_URL);

ws.onopen = function() {
    ws.send('hello');
};

ws.onerror = function() {
    console.log("connection refused")
};

ws.onmessage = function(event) {
    console.log(event.data)
    ws.send('hello')
};

ws.onclose = function(){
    ws.send('close')
    ws.close();
};