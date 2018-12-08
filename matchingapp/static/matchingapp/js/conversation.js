let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
let chat_socket = new WebSocket(ws_scheme + '://' + window.location.host + "/chat/" + window.location.pathname.split('/')[2] + "/");


function sendMsg() {
    let message = {
        command: 'send',
        message: $('#compose').val()
    };
    chat_socket.send(JSON.stringify(message));

}

$(function(){
    scrollDown();
    $("textarea").keyup(function(e){
        if (e.keyCode === 13)
        {
            if (e.shiftKey)
            {
                $('#compos')
            } else {
                sendMsg();
            }
        }
    });
});

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
            document.getElementById('chatHistory').innerHTML = newMsg;
        } else {
            document.getElementById('chatHistory').innerHTML += newMsg;
        }
        scrollDown();
    } else if (resp.data === 'MessageReceived'){
        $('#compose').val("");
    }

};

chat_socket.onclose = function () {
    console.log("Socket closed");
    alert('Connection to chat server has been lost, please reload the page');

};

function scrollDown() {
    let chatHistory = $("#chatHistory");
    chatHistory.scrollTop(chatHistory.height());
}