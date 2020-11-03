// const userName = JSON.parse(document.getElementById('user-name').textContent)
// const roomName = JSON.parse(document.getElementById('room-name').textContent);
console.log(userName)
console.log(roomName)


document.querySelector('#submit').onclick = function (e) {
    console.log('sending data')
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


chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    console.log("YES this")
    if(data.username){
        document.querySelector('#chat-text').innerHTML += ('<span class="text-danger">' + data.username + '</span>'+ ': ' + data.message + '<br/>')
    }
    else{
        document.querySelector('#chat-text').innerHTML += ('<span class="font-weight-bold">' + data.message + '</span>' + '<br/>') 
    }
   
}





$(document).ready(() => {
    $("#exit").click(() => {
        chatSocket.close()
        document.querySelector('#chat-text').innerHTML += ('<span class="font-weight-bold">' + 'Connection closed.' + '</span>' + '<br/>') 
        $("#exit").hide()
        $("#submit").hide()
        $("#reload").show()
    })
    $("#reload").click(() => {
        location.reload()
    })
})