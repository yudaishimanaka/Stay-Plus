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
        if(parseData[i]['avatar'] != "None"){
            $('#flex-container').append('<div class="card text-center" style="width: 15rem; margin-top: 15px; margin-right:15px;"><div class="card-block"><div class="mx-auto imagePreview" style="background-image: url(.' + parseData[i]['avatar'] + ');"></div><h3 class="card-title">' + parseData[i]['user_name'] + '</h3><p class="card-text" style="margin-bottom:0px;">IP:' + parseData[i]['ip_address'] + '</p><p class="card-text">MAC:' + parseData[i]['mac_address'] + '</p></div></div>')
        }else{
            $('#flex-container').append('<div class="card text-center" style="width: 15rem; margin-top: 15px; margin-right:15px;"><div class="card-block"><img src="static/images/profile_sample.png"><h3 class="card-title">' + parseData[i]['user_name'] + '</h3><p class="card-text" style="margin-bottom:0px;">IP:' + parseData[i]['ip_address'] + '</p><p class="card-text">MAC:' + parseData[i]['mac_address'] + '</p></div></div>')
        }
    }
    ws.send('hello')
};

ws.onclose = function(){
    ws.send('close')
    ws.close();
};