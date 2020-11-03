let eraseMode = false
let pos
let toggleBtn, clearBtn
let cnvHeight, cnvWidth
let bgColor = [0, 0, 0]
let cnv
let redDisplay = 'rgba(255, 0, 0, 0.5)'
let red = 'rgb(255, 0, 0)'
let greenDisplay = 'rgba(0, 255, 0, 0.5)'
let green = 'rgb(0, 255, 0)'
let whiteDisplay = 'rgba(255, 255, 255, 0.5)'
let white = 'rgb(255, 255, 255)'
let colorPicker

function setup(){
    let canvasDiv = document.getElementById('sketch-holder')
    let chatAndCanvasDiv = document.getElementById('chatbox')
    cnvHeight = canvasDiv.clientHeight
    cnvWidth = chatAndCanvasDiv.clientWidth
    cnv = createCanvas(cnvWidth, cnvHeight)
    background(bgColor)
    cnv.parent('sketch-holder')

    toggleBtn = createButton("Erase")
    toggleBtn.position(0, 0)
    toggleBtn.parent("sketch-holder")

    clearBtn = createButton("Clear")
    clearBtn.position(60, 0)
    clearBtn.parent("sketch-holder")

    // addStyleToButton(toggleBtn, "btn-success")
    // addStyleToButton(clearBtn, "btn-danger")
    toggleBtn.mouseClicked(() => {
        eraseMode = !eraseMode
        if(eraseMode)
            toggleBtn.html('Draw')
        else
            toggleBtn.html('Erase')
    })

    clearBtn.mouseClicked(() => {
        resetSketch()
    })

    fill('white');
    textSize(16)
    text("Color", 10, 45)

    colorPicker = createColorPicker('#ed225d')
    colorPicker.position(10, 50)
    colorPicker.parent("sketch-holder")

}

function resetSketch(){
    background(bgColor)
    stroke(0, 0, 0)
    fill('white')
    textSize(16)
    text("Color", 10, 45)
}

function addStyleToButton(btn, style) {
    btn.addClass("btn")
    btn.addClass("btn-sm")
    btn.addClass(style)
}

function windowResized() {
    let canvasDiv = document.getElementById('sketch-holder')
    let chatAndCanvasDiv = document.getElementById('chatbox')
    cnvHeight = canvasDiv.clientHeight
    cnvWidth = chatAndCanvasDiv.clientWidth
    resizeCanvas(cnvWidth, cnvHeight)
}

function inside(){
    return (mouseX <= width && mouseX >= 0 && mouseY <= height && mouseY >= 0);
}

function draw(){

    
    frameRate(60)
    strokeWeight(3)
    if(eraseMode && inside()){
        cursor('grab');
    }
    else{
        cursor(CROSS)
    }
    if(drawQueue.length != 0){
        // console.log('drawQueue was not null')
        //draw then set to null, received data from socket mouse position
        let data = drawQueue.shift() //careful, this is not O(1) but O(n); maybe change later? TODO
        let pos = data['mousePos']
        if(data.eraseMode){
            strokeWeight(20)
            stroke(bgColor)
        }
        else{
            stroke(data.color.levels)
        }
        line(pos.mouseX, pos.mouseY, pos.pmouseX, pos.pmouseY)
    }
    if(mouseIsPressed){
        if(!inside()){
            return
        }
        if(eraseMode){
            stroke(bgColor)
        }
        else{
            stroke(colorPicker.color())
        }
        line(mouseX, mouseY, pmouseX, pmouseY);
        chatSocket.send(JSON.stringify({'type': 'canvas',
            'data': {    
                'mousePos': {
                    mouseX, mouseY, pmouseX, pmouseY
                },
                'color': colorPicker.color(),
                eraseMode
            }
        }))
    }

}