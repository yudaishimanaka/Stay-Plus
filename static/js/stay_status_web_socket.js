var WS_URL = "ws://localhost:8888/ws/"

var ws = new WebSocket(WS_URL);

ws.onopen = function() {
    ws.send('hello');
};

ws.onerror = function() {
    console.log("connection refused")
};

ws.onmessage = function(event) {
    parseData = JSON.parse(event.data)
    $('#flex-container').html("")
    for(i=0; i < parseData.length; i++){
       $('#flex-container').append('<div class="card" style="width: 15rem; margin-top: 15px; margin-right:15px;"><div class="card-block"><h3 class="card-title">' + parseData[i]['user_name'] + '</h3><p class="card-text">IP:' + parseData[i]['ip_address'] + '</p><p class="card-text">MAC:' + parseData[i]['mac_address'] + '</p></div></div>')
    }
    ws.send('hello')
};

ws.onclose = function(){
    ws.send('close')
    ws.close();
};