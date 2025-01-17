// -------------- Initialize drawing --------------
var width = window.innerWidth * 0.95;
var height = window.innerHeight * 0.95;

var stage = new Konva.Stage({
    container: 'container',
    width: width,
    height: height,
});

var layerObjects = new Konva.Layer();
stage.add(layerObjects);
var layerTexts = new Konva.Layer();
stage.add(layerTexts);

// -------------- Connect to Python websocket --------------
var registeredComps = []
var isRegistered = new Array(10).fill(false)
var names = ["StraightRoad", "Turn90", "Checkpoint", "Wall", "Booster", "Refuel", "Ice", "Mud", "Decoration", "Car"]
const ws = new WebSocket("ws://localhost:8000");
ws.onopen = () => {
    ws.send("USER BATUHAN")
    ws.send("GET_REGISTERED_COMPS")
}
var timerId;
ws.onmessage = event => {
    const msg = event.data

    if (!(msg.includes("[") || msg.includes("Username set to"))) {
        notification.setAttr("text", msg)
        clearTimeout(timerId)
        timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
    }
    
    if (msg.includes("[")) {
        registeredComps = JSON.parse(msg)
        registeredComps.forEach((e, i) => {
            const index = names.indexOf(e)
            if (index !== -1) {
                isRegistered[index] = true
            }
        })
        isRegistered.forEach((e, i) => {
            if (e)
                comps[i].x(comps[i].x() + 415)
        })
    }
}

// -------------- Draw texts --------------
var notification = new Konva.Text({
    x: 10,
    y: 10,
    text: '',
    fontSize: 30,
    fontFamily: 'Calibri',
    fill: 'black',
})
layerTexts.add(notification)

var unregistered = new Konva.Text({
    x: 10,
    y: 50,
    text: "Unregistered Components",
    fontSize: 30,
    fontFamily: 'Arial',
    fill: 'black',
})
layerTexts.add(unregistered)

var registered = new Konva.Text({
    x: 450,
    y: 50,
    text: "Registered Components",
    fontSize: 30,
    fontFamily: 'Arial',
    fill: 'black',
})
layerTexts.add(registered)

// -------------- Draw line --------------
var line = new Konva.Line({
    points: [400, 50, 400, 400],
    stroke: 'black',
    strokeWidth: 5,
    lineCap: 'round',
    lineJoin: 'round',
});
layerObjects.add(line)

// -------------- Draw components --------------
var comps = []

var straightRoad = new Konva.Image({
    x: 150,
    y: 180,
    width: 65,
    height: 65,
});
comps.push(straightRoad)

var turn90 = new Konva.Image({
    x: 150,
    y: 100,
    width: 65,
    height: 65,
});
comps.push(turn90)

var checkpoint = new Konva.Image({
    x: 150,
    y: 260,
    width: 65,
    height: 65,
});
comps.push(checkpoint)

var wall = new Konva.Image({
    x: 80,
    y: 180,
    width: 65,
    height: 65,
});
comps.push(wall)

var booster = new Konva.Image({
    x: 80,
    y: 260,
    width: 65,
    height: 65,
});
comps.push(booster)

var refuel = new Konva.Image({
    x: 220,
    y: 100,
    width: 65,
    height: 65,
});
comps.push(refuel)

var ice = new Konva.Image({
    x: 220,
    y: 180,
    width: 65,
    height: 65,
});
comps.push(ice)

var mud = new Konva.Image({
    x: 220,
    y: 260,
    width: 65,
    height: 65,
});
comps.push(mud)

var decoration = new Konva.Image({
    x: 80,
    y: 100,
    width: 65,
    height: 65,
});
comps.push(decoration)

var porsche = new Konva.Image({
    x: 182,
    y: 360,
    width: 48,
    height: 25,
    draggable: true,
    offset: {
        x: 24,
        y: 12.5,
    },
});
comps.push(porsche)

comps.forEach((comp, index) => {
    layerObjects.add(comp)
    
    var imgObj = new Image()
    imgObj.onload = () => {
        comp.image(imgObj)
    }
    if (names[index] == "Car")
        imgObj.src = `./images/Porsche.png`
    else
        imgObj.src = `./images/${names[index]}.png`

    comp.on('mouseover', () => document.body.style.cursor = 'pointer')
    comp.on('mouseout', () => document.body.style.cursor = 'default')

    comp.on("click", () => {
        if (!isRegistered[index]) {
            ws.send(`REGISTER_COMP ${names[index]}`)
            comp.x(comp.x() + 415)
            isRegistered[index] = true
        } else {
            ws.send(`UNREGISTER_COMP ${names[index]}`)
            comp.x(comp.x() - 415)
            isRegistered[index] = false
        }
    })
})