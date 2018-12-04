let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
let chat_socket = new WebSocket(ws_scheme + '://' + window.location.host + "/chat/" + window.location.pathname.split('/')[2] + "/");
$("#chatHistory").scrollTop($("#chatHistory").height());

function sendMsg() {
    let message = {
        command: 'send',
        message: $('#compose').val()
    };
    chat_socket.send(JSON.stringify(message));

}

chat_socket.onopen = function (evt) {
    console.log("Connected to websocket!");
    console.log(evt);
    chat_socket.send(JSON.stringify({command: 'join', convoID: window.location.pathname.split('/')[2]}))
};

chat_socket.onmessage = function(resp) {
    console.log(resp);
    if ((resp.data !== 'ConnectionSuccessful') && (resp.data !== 'MessageReceived'))
    {
        let data = JSON.parse(resp.data);
        console.log(data);
        let newMsg = data.text.sender + " @ " + data.text.sent_at + ": " + data.text.contents + "<br />";
        if (document.getElementById('chatHistory').innerHTML.replace(/\r?\s|\r/g, "") === "Nomessagessentyet,sendonenow")
        {
            document.getElementById('chatHistory').innerHTML = newMsg + "<br />";
        } else {
            document.getElementById('chatHistory').innerHTML += newMsg + "<br />";
        }
    } else if (resp.data === 'MessageReceived'){
        $('#compose').val("");
    }

};

chat_socket.onclose = function () {
    console.log("Socket closed");
    alert('Connection to chat server has been lost, please reload the page');

};