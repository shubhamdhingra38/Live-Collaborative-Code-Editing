var editor = ace.edit("editor");
editor.setTheme("ace/theme/twilight");
document.getElementById('editor').style.fontSize='14px';

console.log(userName)


editor.session.setMode("ace/mode/python");
let cursorPos = null;
let lock = false



//send updates from text editor to other people connected using websocket
//this will be done as soon as a keystroke is made
editor.session.on('change', function(delta) {
    // console.log(lock)
    if(lock) return;
// delta.start, delta.end, delta.lines, delta.action
// console.log(delta)
// editor.getSession().getDocument().applyDeltas(delta)
chatSocket.send(JSON.stringify({"type": "editor", "text": delta, "cursor": editor.selection.getCursor()}))
});


chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if(data['type']=='chat'){
        if(data.username){
            document.querySelector('#chat-text').innerHTML += ('<span class="text-danger">' + data.username + '</span>'+ ': ' + data.message + '<br/>')
        }
        else{
            document.querySelector('#chat-text').innerHTML += ('<span class="font-weight-bold">' + data.message + '</span>' + '<br/>') 
        }
    }
    else if(data['type']=='editor'){
        if(userName!=data.username){
            cursorPos = editor.selection.getCursor();
            // console.log(cursorPos, 'is the cursor at')
            lock = true;
            if(data['text']!=null){
                editor.getSession().getDocument().applyDeltas([data['text']])
                // editor.moveCursorTo(5,5);
                // editor.moveCursorToPosition(3,0);
    
            }
            lock = false;
            editor.moveCursorToPosition(cursorPos)
            
    
        }
        else{
            console.log("no username")
        }
    }
    // console.log(data)
   
}

// $(document).ready(() => {
//     // $("#editor").on('input change keyup', () => {
//     //     console.log(editor.getValue())
//     //     console.log(editor.selection.getCursor())
//     //     chatSocket.send(JSON.stringify({"text": editor.getValue(), "cursor": editor.selection.getCursor()}))                
//     // })
// })
