let eraseMode = false
let pos
let toggleBtn
let cnvHeight, cnvWidth
let bgColor = [0, 0, 0]
let strokeColor = [255, 0, 0]


function setup(){
    let canvasDiv = document.getElementById('sketch-holder')
    let chatAndCanvasDiv = document.getElementById('chatbox')
    cnvHeight = canvasDiv.clientHeight
    cnvWidth = chatAndCanvasDiv.clientWidth
    let cnv = createCanvas(cnvWidth, cnvHeight)
    background(bgColor)
    cnv.parent('sketch-holder')

    toggleBtn = createButton("Toggle erase")
    toggleBtn.position(0, 0)
    toggleBtn.parent("sketch-holder")
    toggleBtn.mouseClicked(() => {
        eraseMode = !eraseMode
    }); 
}

function windowResized() {
    let canvasDiv = document.getElementById('sketch-holder')
    let chatAndCanvasDiv = document.getElementById('chatbox')
    cnvHeight = canvasDiv.clientHeight
    cnvWidth = chatAndCanvasDiv.clientWidth
    resizeCanvas(cnvWidth, cnvHeight)
}

function draw(){
    frameRate(60)
    strokeWeight(5)
    if(drawQueue.length != 0){
        console.log('drawQueue was not null')
        //draw then set to null, received data from socket mouse position
        let data = drawQueue.shift() //careful, this is not O(1) but O(n); maybe change later? TODO
        let pos = data['mousePos']
        if(data.eraseMode){
            stroke(bgColor)
        }
        else{
            stroke(strokeColor)
        }
        line(pos.mouseX, pos.mouseY, pos.pmouseX, pos.pmouseY)
    }
    if(mouseIsPressed){
        if(eraseMode){
            stroke(bgColor)
        }
        else{
            stroke(strokeColor)
        }
        line(mouseX, mouseY, pmouseX, pmouseY);
        chatSocket.send(JSON.stringify({'type': 'canvas',
            'data': {    
                'mousePos': {
                    mouseX, mouseY, pmouseX, pmouseY
                },
                eraseMode
            }
        }))
    }

}