let eraseMode = false
let pos
let toggleBtn



function setup(){
    let cnv = createCanvas(500, 500)
    background(200)
    cnv.parent('sketch-holder')

    toggleBtn = createButton("Toggle erase")
    toggleBtn.position(0, 0)
    toggleBtn.parent("sketch-holder")
    toggleBtn.mouseClicked(() => {
        eraseMode = !eraseMode
    }); 
}


function draw(){
    frameRate(60)
    strokeWeight(5)
    stroke(255)
    if(drawQueue.length != 0){
        console.log('drawQueue was not null')
        //draw then set to null, received data from socket mouse position
        let pos = drawQueue.shift() //careful, this is not O(1) but O(n); maybe change later? TODO
        line(pos.mouseX, pos.mouseY, pos.pmouseX, pos.pmouseY)
    }
    if(mouseIsPressed){
        if(eraseMode){
            stroke(200)
        }
        else{
            stroke(255)
        }
        line(mouseX, mouseY, pmouseX, pmouseY);
        chatSocket.send(JSON.stringify({'type': 'canvas',
            'data': {    
                'mousePos': {
                    mouseX, mouseY, pmouseX, pmouseY
                }
                
            }
        }))
    }

}