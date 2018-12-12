/*
    Once the document is loaded, a keyup listener is added to the compose text area to allow the user to send with an Enter
    press, unless the Shift key is pressed, when it allows the user to multiple lines. It also ensures that the scroll
    box is at the bottom by default so that the user sees the latest messages
 */

$(function(){
    scrollDown();
    $("textarea").keyup(function(e){
        if (e.keyCode === 13)
        {
            if (!e.shiftKey)
            {
                sendMsg();
            }
        }
    });
});


/*
    A WebSocket connection is needed in order to have instant messaging so a connection is
    immediately opened on start up. Once the connection is opened, it sends the conversation id to the server to
    join the correct channel group.
 */

let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
let chat_socket = new WebSocket(ws_scheme + '://' + window.location.host + "/chat/" + window.location.pathname.split('/')[2] + "/");

// When the user sends a message, a message is sent through the WebSocket to the server. That then sends a confirmation
// which is handled further down
function sendMsg() {
    let message = {
        command: 'send',
        message: $('#compose').val().trim()
    };
    chat_socket.send(JSON.stringify(message));

}

// When the WebSocket connection is opened, a join message is sent to join the connection to the correct channel group
chat_socket.onopen = function (evt) {
    console.log("Connected to websocket!");
    console.log(evt);
    chat_socket.send(JSON.stringify({command: 'join', convoID: window.location.pathname.split('/')[2]}))
};


/*
    When the server sends a message through the channel, there are three types. The first is ConnectionSuccessful, which
    means that the WebSocket is connected successfully. The second is MessageReceived, which means that the user's
    message was received successfully and added to the database, when this is received, it clears the contents of the
    compose textarea. The final is a normal message receive, this then added to the messages scroll box
 */
chat_socket.onmessage = function(resp) {
    console.log(resp);
    if ((resp.data !== 'ConnectionSuccessful') && (resp.data !== 'MessageReceived'))
    {
        let data = JSON.parse(resp.data);
        console.log(data.text.contents);
        let newMsg = data.text.sender + " @ " + data.text.sent_at + ": " + data.text.contents + "\n";
        console.log(newMsg);
        if (document.getElementById('chatHistory').innerText.replace(/\r?\s|\r/g, "") === "Nomessagessentyet,sendonenow")
        {
            document.getElementById('chatHistory').innerText = newMsg;
        } else {
            document.getElementById('chatHistory').innerText += newMsg;
        }
        scrollDown();
    } else if (resp.data === 'MessageReceived'){
        $('#compose').val("");
    }

};


// When the connection is closed, the user is alerted to the error and told to reload the page, to reconnect
chat_socket.onclose = function () {
    console.log("Socket closed");
    alert('Connection to chat server has been lost, please reload the page');

};

// Function to scroll the message box to the bottom
function scrollDown() {
    let chatHistory = $("#chatHistory");
    chatHistory.scrollTop(chatHistory.height());
}