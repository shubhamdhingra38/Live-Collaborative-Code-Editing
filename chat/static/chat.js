const userName = JSON.parse(document.getElementById('user-name').textContent)
const roomName = JSON.parse(document.getElementById('room-name').textContent);
console.log(userName)
console.log(roomName)


document.querySelector('#submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'type': 'chat',
        'message': message,
    }));
    messageInputDom.value = '';
};




const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    roomName +
    '/'
);


$(document).ready(() => {
    $("#exit").click(() => {
        chatSocket.close()
        document.querySelector('#chat-text').innerHTML += ('<span class="font-weight-bold">' + 'Connection closed.' + '</span>' + '<br/>') 
    })
})