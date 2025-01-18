var mapId;

window.onload = () => {
    var url = document.location.href
    mapId = url.split('?')[1].split("=")[1]
}

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

var rankingTexts = []
var registeredComps = []
var aliveCars = []
var activeCar = -1
var carIds = []
var carRankings = []
var map;

// -------------- Connect to Python websocket --------------
var timerId;
const ws = new WebSocket("ws://localhost:8000");
ws.onopen = () => {
    ws.send("USER BATUHAN")
    ws.send("GET_REGISTERED_COMPS")
    ws.send(`ATTACH_MAP ${mapId}`)
    ws.send(`SAVE ${mapId}`)
    ws.send(`LOAD_MAP ${mapId}`)


    ws.send(`START_GAME ${mapId}`)
}
ws.onmessage = event => {
    const msg = event.data
    if (!(msg.startsWith("{") || msg.startsWith("[") || msg.includes("Car Rankings")|| msg.includes("Game saved") || msg.includes("Username set to") || (msg.includes("Car with id") && msg.includes("does not exist")))) {
        notification.setAttr("text", msg)
        clearTimeout(timerId)
        timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
    }
    
    if (msg.includes("Created car with id")) {
        carIds.push(msg.split(" ")[4].substring(0, msg.split(" ")[4].length - 1))
    } else if (msg.includes("Deleted car with id")) {
        carIds.splice(carIds.indexOf(msg.split(" ")[4].substring(0, msg.split(" ")[4].length - 1)), 1)
    } else if (msg.includes("{\"cols\":")) {
        map = JSON.parse(msg)
        map.cells.forEach(cell => {
            var comp = new Konva.Image({
                x: 800 + cell.col * 65 + 32.5,
                y: 10 + cell.row * 65 + 32.5,
                width: 65,
                height: 65,
                offset: {
                    x: 32.5,
                    y: 32.5,
                },
                rotation: cell.rotation * 90
            });
            comp.on('mouseover', () => document.body.style.cursor = 'pointer')
            comp.on('mouseout', () => document.body.style.cursor = 'default')
            layerObjects.add(comp);
            var imageObj = new Image();
            imageObj.onload = function () {
                comp.image(this)
            };
            imageObj.src = `./images/${cell.type}.png`;
            comp.on("click", () => {
                comp.destroy()
                ws.send(`DELETE_COMP ${mapId} ${cell.col} ${cell.row}`)
            })
            comp.on("wheel", () => {
                comp.rotate(90)
                ws.send(`ROTATE_COMP ${mapId} ${cell.col} ${cell.row}`)
            })
        })
        map.cars.forEach(car => {
            carIds.push(car.id.toString())
        })
        map.cars.forEach(car => {
            switch (car.model) {
                case "Porsche":
                    porsche.setAttr("x", 800 + 32.5 + (car.pos[0] / map.cellsize) * 65)
                    porsche.setAttr("y", 10 + 32.5 + (car.pos[1] / map.cellsize) * 65)
                    porsche.setAttr("draggable", false)
        
                    porsche.on("click", () => {
                        ws.send(`DELETE_CAR ${mapId} ${carIds[aliveCars.indexOf(porsche)]}`)
                        if (activeCar == aliveCars.indexOf(porsche))
                            activeCar = -1
                        aliveCars.splice(aliveCars.indexOf(porsche), 1)
                        
                        porsche.off("click")
                        porsche.position({ x: 112.5, y: 460 })
                        porsche.rotation(0)
                        porsche.setAttr("draggable", true)
                    })
                    aliveCars.push(porsche)
                    break;
                case "Bmw":
                    bmw.setAttr("x", 800 + 32.5 + (car.pos[0] / map.cellsize) * 65)
                    bmw.setAttr("y", 10 + 32.5 + (car.pos[1] / map.cellsize) * 65)
                    bmw.setAttr("draggable", false)

                    bmw.on("click", () => {
                        ws.send(`DELETE_CAR ${mapId} ${carIds[aliveCars.indexOf(bmw)]}`)
                        if (activeCar == aliveCars.indexOf(bmw))
                            activeCar = -1
                        aliveCars.splice(aliveCars.indexOf(bmw), 1)
                        
                        bmw.off("click")
                        bmw.position({ x: 112.5, y: 504 })
                        bmw.rotation(0)
                        bmw.setAttr("draggable", true)
                    })
                    aliveCars.push(bmw)
                    break
                case "Lamborghini":
                    lambo.setAttr("x", 800 + 32.5 + (car.pos[0] / map.cellsize) * 65)
                    lambo.setAttr("y", 10 + 32.5 + (car.pos[1] / map.cellsize) * 65)
                    lambo.setAttr("draggable", false)

                    lambo.on("click", () => {
                        ws.send(`DELETE_CAR ${mapId} ${carIds[aliveCars.indexOf(lambo)]}`)
                        if (activeCar == aliveCars.indexOf(lambo))
                            activeCar = -1
                        aliveCars.splice(aliveCars.indexOf(lambo), 1)
                        
                        lambo.off("click")
                        lambo.position({ x: 112.5, y: 544 })
                        lambo.rotation(0)
                        lambo.setAttr("draggable", true)
                    })
                    aliveCars.push(lambo)
                    break
                case "Ferrari":
                    ferr.setAttr("x", 800 + 32.5 + (car.pos[0] / map.cellsize) * 65)
                    ferr.setAttr("y", 10 + 32.5 + (car.pos[1] / map.cellsize) * 65)
                    ferr.setAttr("draggable", false)

                    ferr.on("click", () => {
                        ws.send(`DELETE_CAR ${mapId} ${carIds[aliveCars.indexOf(ferr)]}`)
                        if (activeCar == aliveCars.indexOf(ferr))
                            activeCar = -1
                        aliveCars.splice(aliveCars.indexOf(ferr), 1)

                        ferr.off("click")
                        ferr.position({ x: 112.5, y: 584 })
                        ferr.rotation(0)
                        ferr.setAttr("draggable", true)
                    })
                    aliveCars.push(ferr)
                    break
                case "Ford":
                    ford.setAttr("x", 800 + 32.5 + (car.pos[0] / map.cellsize) * 65)
                    ford.setAttr("y", 10 + 32.5 + (car.pos[1] / map.cellsize) * 65)
                    ford.setAttr("draggable", false)

                    ford.on("click", () => {
                        ws.send(`DELETE_CAR ${mapId} ${carIds[aliveCars.indexOf(ford)]}`)
                        if (activeCar == aliveCars.indexOf(ford))
                            activeCar = -1
                        aliveCars.splice(aliveCars.indexOf(ford), 1)

                        ford.off("click")
                        ford.position({ x: 112.5, y: 624 })
                        ford.rotation(0)
                        ford.setAttr("draggable", true)
                    })
                    aliveCars.push(ford)
                    break
            }
        })
    } else if (msg.includes("{\"id\":")) {
        const car_info = JSON.parse(msg)
        const dx = (9 - 0) / (1000 - 0)
        const dy = (9 - 0) / (1000 - 0)
        const x = Math.round((Math.floor(car_info.x) - 0) * dx)
        const y = Math.round((Math.floor(car_info.y) - 0) * dy)
        aliveCars[carIds.indexOf(car_info.id.toString())].setAttr("x", 832.5 + x * 65)
        aliveCars[carIds.indexOf(car_info.id.toString())].setAttr("y", 42.5 + y * 65)
        aliveCars[carIds.indexOf(car_info.id.toString())].rotation(-car_info.angle)
    } else if (msg.includes("Car Rankings")) {
        const temp = msg.substring(msg.indexOf("Car Rankings") + 13, msg.length).split("\n")
        var rankingArr = temp.slice(1, temp.length - 1)

        if (rankingArr.length > 0) {
            rankingTexts.forEach(t => t.destroy())
            rankingTexts = []
            rankingArr.unshift("------------------- Car Rankings -------------------")
            rankingArr.forEach((str, index) => {
                const text = new Konva.Text({
                  x: 10,
                  y: 50 + index * 25,
                  text: str,
                  fontSize: 20,
                  fontFamily: 'Arial',
                  fill: 'black',
                });

                rankingTexts.push(text)
                layerTexts.add(text);
            });
        } else {
            rankingTexts.forEach(t => t.destroy())
            rankingTexts = []
        }
    }  else if (msg.includes("[")) {
        registeredComps = JSON.parse(msg)
    }
}

// -------------- Get car and ranking info, save every 100 ms --------------
window.setInterval(() => {
    if (ws.readyState == WebSocket.OPEN) {
        carIds.forEach(id => {
            ws.send(`CAR_INFO ${mapId} ${id}`)
            aliveCars[carIds.indexOf(id)].moveToTop()
        })
        ws.send(`DRAW_MAP ${mapId}`)
        ws.send(`SAVE ${mapId}`)
    }
}, 10)

// -------------- Draw notification text --------------
var notification = new Konva.Text({
    x: 10,
    y: 10,
    text: '',
    fontSize: 30,
    fontFamily: 'Calibri',
    fill: 'black',
})
layerTexts.add(notification)

// -------------- Draw the map --------------
var map = new Konva.Rect({
    x: 800,
    y: 10,
    width: 650,
    height: 650,
    fill: "white",
    cornerRadius: 10,
});
layerObjects.add(map);

// -------------- Draw the frame of the map --------------
for (i = 0; i <= 10; i++) {
    points = [800 + i * 65, 10, 800 + i * 65, 10 + 10 * 65]
    var line = new Konva.Line({
        points: points,
        stroke: "black",
        strokeWidth: 1,
        lineCap: 'round',
        lineJoin: 'round',
    });
    layerObjects.add(line)
}
for (i = 0; i <= 10; i++) {
    points = [800, 10 + i * 65, 800 + 10 * 65, 10 + i * 65]
    var line = new Konva.Line({
        points: points,
        stroke: "black",
        strokeWidth: 1,
        lineCap: 'round',
        lineJoin: 'round',
    });
    layerObjects.add(line)
}

// -------------- Draw components --------------
var straightRoad = new Konva.Image({
    x: 80,
    y: 280,
    width: 65,
    height: 65,
    draggable: true,
});
straightRoad.on('mouseover', () => document.body.style.cursor = 'pointer')
straightRoad.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(straightRoad);
var imageObj = new Image();
imageObj.onload = function () {
    straightRoad.image(this)
};
imageObj.src = `./images/StraightRoad.png`;
straightRoad.on("dragend", () => {
    if (straightRoad.attrs.x + 32.5 >= 800 && straightRoad.attrs.x + 32.5 <= 1450 && straightRoad.attrs.y + 32.5 >= 10 && straightRoad.attrs.y + 32.5 <= 650) {
        if (registeredComps.includes("StraightRoad")) {
            var dx = (9 - 0) / (1417.5 - 767.5)
            var dy = (9 - 0) / (617.5 - (-22.5))
            var x = Math.round((Math.floor(straightRoad.attrs.x) - 767.5) * dx)
            var y = Math.round((Math.floor(straightRoad.attrs.y) - (-22.5)) * dy)
            ws.send(`CREATE_COMP ${mapId} StraightRoad ${x} ${y}`)

            var newStraightRoad = new Konva.Image({
                x: 800 + x * 65 + 32.5,
                y: 10 + y * 65 + 32.5,
                width: 65,
                height: 65,
                offset: {
                    x: 32.5,
                    y: 32.5,
                },
            });
            newStraightRoad.on('mouseover', () => document.body.style.cursor = 'pointer')
            newStraightRoad.on('mouseout', () => document.body.style.cursor = 'default')
            layerObjects.add(newStraightRoad);
            var imageObj = new Image();
            imageObj.onload = function () {
                newStraightRoad.image(this)
            };
            imageObj.src = `./images/StraightRoad.png`;
            newStraightRoad.on("click", () => {
                newStraightRoad.destroy()
                ws.send(`DELETE_COMP ${mapId} ${x} ${y}`)
            })
            newStraightRoad.on("wheel", () => {
                newStraightRoad.rotate(90)
                ws.send(`ROTATE_COMP ${mapId} ${x} ${y}`)
            })
        }
        else {
            notification.setAttr("text", "Component 'StraightRoad' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    }
    
    straightRoad.position({ x: 80, y: 280 })
})

var turn90 = new Konva.Image({
    x: 80,
    y: 200,
    width: 65,
    height: 65,
    draggable: true,
});
turn90.on('mouseover', () => document.body.style.cursor = 'pointer')
turn90.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(turn90);
var imageObj = new Image();
imageObj.onload = function () {
    turn90.image(this)
};
imageObj.src = `./images/Turn90.png`;
turn90.on("dragend", () => {
    if (turn90.attrs.x + 32.5 >= 800 && turn90.attrs.x + 32.5 <= 1450 && turn90.attrs.y + 32.5 >= 10 && turn90.attrs.y + 32.5 <= 650) {
        if (registeredComps.includes("Turn90")) {
            var dx = (9 - 0) / (1417.5 - 767.5)
            var dy = (9 - 0) / (617.5 - (-22.5))
            var x = Math.round((Math.floor(turn90.attrs.x) - 767.5) * dx)
            var y = Math.round((Math.floor(turn90.attrs.y) - (-22.5)) * dy)
            ws.send(`CREATE_COMP ${mapId} Turn90 ${x} ${y}`)

            var newTurn90 = new Konva.Image({
                x: 800 + x * 65 + 32.5,
                y: 10 + y * 65 + 32.5,
                width: 65,
                height: 65,
                offset: {
                    x: 32.5,
                    y: 32.5,
                },
            });
            newTurn90.on('mouseover', () => document.body.style.cursor = 'pointer')
            newTurn90.on('mouseout', () => document.body.style.cursor = 'default')
            layerObjects.add(newTurn90);
            var imageObj = new Image();
            imageObj.onload = function () {
                newTurn90.image(this)
            };
            imageObj.src = `./images/Turn90.png`;
            newTurn90.on("click", () => {
                newTurn90.destroy()
                ws.send(`DELETE_COMP ${mapId} ${x} ${y}`)
            })
            newTurn90.on("wheel", () => {
                newTurn90.rotate(90)
                ws.send(`ROTATE_COMP ${mapId} ${x} ${y}`)
            })
        }
        else {
            notification.setAttr("text", "Component 'Turn90' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    }
    turn90.position({ x: 80, y: 200 })
})

var checkpoint = new Konva.Image({
    x: 80,
    y: 360,
    width: 65,
    height: 65,
    draggable: true,
});
checkpoint.on('mouseover', () => document.body.style.cursor = 'pointer')
checkpoint.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(checkpoint);
var imageObj = new Image();
imageObj.onload = function () {
    checkpoint.image(this)
};
imageObj.src = `./images/Checkpoint.png`;
checkpoint.on("dragend", () => {
    if (checkpoint.attrs.x + 32.5 >= 800 && checkpoint.attrs.x + 32.5 <= 1450 && checkpoint.attrs.y + 32.5 >= 10 && checkpoint.attrs.y + 32.5 <= 650) {
        if (registeredComps.includes("Checkpoint")) {
            var dx = (9 - 0) / (1417.5 - 767.5)
            var dy = (9 - 0) / (617.5 - (-22.5))
            var x = Math.round((Math.floor(checkpoint.attrs.x) - 767.5) * dx)
            var y = Math.round((Math.floor(checkpoint.attrs.y) - (-22.5)) * dy)
            ws.send(`CREATE_COMP ${mapId} Checkpoint ${x} ${y}`)

            var newCheckpoint = new Konva.Image({
                x: 800 + x * 65 + 32.5,
                y: 10 + y * 65 + 32.5,
                width: 65,
                height: 65,
                offset: {
                    x: 32.5,
                    y: 32.5,
                },
            });
            newCheckpoint.on('mouseover', () => document.body.style.cursor = 'pointer')
            newCheckpoint.on('mouseout', () => document.body.style.cursor = 'default')
            layerObjects.add(newCheckpoint);
            var imageObj = new Image();
            imageObj.onload = function () {
                newCheckpoint.image(this)
            };
            imageObj.src = `./images/Checkpoint.png`;
            newCheckpoint.on("click", () => {
                newCheckpoint.destroy()
                ws.send(`DELETE_COMP ${mapId} ${x} ${y}`)
            })
            newCheckpoint.on("wheel", () => {
                newCheckpoint.rotate(90)
                ws.send(`ROTATE_COMP ${mapId} ${x} ${y}`)
            })
        }
        else {
            notification.setAttr("text", "Component 'Checkpoint' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    }
    checkpoint.position({ x: 80, y: 360 })
})

var wall = new Konva.Image({
    x: 10,
    y: 280,
    width: 65,
    height: 65,
    draggable: true,
});
wall.on('mouseover', () => document.body.style.cursor = 'pointer')
wall.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(wall);
var imageObj = new Image();
imageObj.onload = function () {
    wall.image(this)
};
imageObj.src = `./images/Wall.png`;
wall.on("dragend", () => {
    if (wall.attrs.x + 32.5 >= 800 && wall.attrs.x + 32.5 <= 1450 && wall.attrs.y + 32.5 >= 10 && wall.attrs.y + 32.5 <= 650) {
        if (registeredComps.includes("Wall")) {
            var dx = (9 - 0) / (1417.5 - 767.5)
            var dy = (9 - 0) / (617.5 - (-22.5))
            var x = Math.round((Math.floor(wall.attrs.x) - 767.5) * dx)
            var y = Math.round((Math.floor(wall.attrs.y) - (-22.5)) * dy)
            ws.send(`CREATE_COMP ${mapId} Wall ${x} ${y}`)

            var newWall = new Konva.Image({
                x: 800 + x * 65 + 32.5,
                y: 10 + y * 65 + 32.5,
                width: 65,
                height: 65,
                offset: {
                    x: 32.5,
                    y: 32.5,
                },
            });
            newWall.on('mouseover', () => document.body.style.cursor = 'pointer')
            newWall.on('mouseout', () => document.body.style.cursor = 'default')
            layerObjects.add(newWall);
            var imageObj = new Image();
            imageObj.onload = function () {
                newWall.image(this)
            };
            imageObj.src = `./images/Wall.png`;
            newWall.on("click", () => {
                newWall.destroy()
                ws.send(`DELETE_COMP ${mapId} ${x} ${y}`)
            })
            newWall.on("wheel", () => {
                newWall.rotate(90)
                ws.send(`ROTATE_COMP ${mapId} ${x} ${y}`)
            })
        }
        else {
            notification.setAttr("text", "Component 'Wall' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    }
    wall.position({ x: 10, y: 280 })
})

var booster = new Konva.Image({
    x: 10,
    y: 360,
    width: 65,
    height: 65,
    draggable: true,
});
booster.on('mouseover', () => document.body.style.cursor = 'pointer')
booster.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(booster);
var imageObj = new Image();
imageObj.onload = function () {
    booster.image(this)
};
imageObj.src = `./images/Booster.png`;
booster.on("dragend", () => {
    if (booster.attrs.x + 32.5 >= 800 && booster.attrs.x + 32.5 <= 1450 && booster.attrs.y + 32.5 >= 10 && booster.attrs.y + 32.5 <= 650) {
        if (registeredComps.includes("Booster")) {
            var dx = (9 - 0) / (1417.5 - 767.5)
            var dy = (9 - 0) / (617.5 - (-22.5))
            var x = Math.round((Math.floor(booster.attrs.x) - 767.5) * dx)
            var y = Math.round((Math.floor(booster.attrs.y) - (-22.5)) * dy)
            ws.send(`CREATE_COMP ${mapId} Booster ${x} ${y}`)

            var newBooster = new Konva.Image({
                x: 800 + x * 65 + 32.5,
                y: 10 + y * 65 + 32.5,
                width: 65,
                height: 65,
                offset: {
                    x: 32.5,
                    y: 32.5,
                },
            });
            newBooster.on('mouseover', () => document.body.style.cursor = 'pointer')
            newBooster.on('mouseout', () => document.body.style.cursor = 'default')
            layerObjects.add(newBooster);
            var imageObj = new Image();
            imageObj.onload = function () {
                newBooster.image(this)
            };
            imageObj.src = `./images/Booster.png`;
            newBooster.on("click", () => {
                newBooster.destroy()
                ws.send(`DELETE_COMP ${mapId} ${x} ${y}`)
            })
            newBooster.on("wheel", () => {
                newBooster.rotate(90)
                ws.send(`ROTATE_COMP ${mapId} ${x} ${y}`)
            })
        }
        else {
            notification.setAttr("text", "Component 'Booster' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    }
    booster.position({ x: 10, y: 360 })
})

var refuel = new Konva.Image({
    x: 10,
    y: 440,
    width: 65,
    height: 65,
    draggable: true,
});
refuel.on('mouseover', () => document.body.style.cursor = 'pointer')
refuel.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(refuel);
var imageObj = new Image();
imageObj.onload = function () {
    refuel.image(this)
};
imageObj.src = `./images/Refuel.png`;
refuel.on("dragend", () => {
    if (refuel.attrs.x + 32.5 >= 800 && refuel.attrs.x + 32.5 <= 1450 && refuel.attrs.y + 32.5 >= 10 && refuel.attrs.y + 32.5 <= 650) {
        if (registeredComps.includes("Refuel")) {
            var dx = (9 - 0) / (1417.5 - 767.5)
            var dy = (9 - 0) / (617.5 - (-22.5))
            var x = Math.round((Math.floor(refuel.attrs.x) - 767.5) * dx)
            var y = Math.round((Math.floor(refuel.attrs.y) - (-22.5)) * dy)
            ws.send(`CREATE_COMP ${mapId} Refuel ${x} ${y}`)

            var newRefuel = new Konva.Image({
                x: 800 + x * 65 + 32.5,
                y: 10 + y * 65 + 32.5,
                width: 65,
                height: 65,
                offset: {
                    x: 32.5,
                    y: 32.5,
                },
            });
            newRefuel.on('mouseover', () => document.body.style.cursor = 'pointer')
            newRefuel.on('mouseout', () => document.body.style.cursor = 'default')
            layerObjects.add(newRefuel);
            var imageObj = new Image();
            imageObj.onload = function () {
                newRefuel.image(this)
            };
            imageObj.src = `./images/Refuel.png`;
            newRefuel.on("click", () => {
                newRefuel.destroy()
                ws.send(`DELETE_COMP ${mapId} ${x} ${y}`)
            })
            newRefuel.on("wheel", () => {
                newRefuel.rotate(90)
                ws.send(`ROTATE_COMP ${mapId} ${x} ${y}`)
            })
        }
        else {
            notification.setAttr("text", "Component 'Refuel' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    }
    refuel.position({ x: 10, y: 440 })
})

var ice = new Konva.Image({
    x: 10,
    y: 520,
    width: 65,
    height: 65,
    draggable: true,
});
ice.on('mouseover', () => document.body.style.cursor = 'pointer')
ice.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(ice);
var imageObj = new Image();
imageObj.onload = function () {
    ice.image(this)
};
imageObj.src = `./images/Ice.png`;
ice.on("dragend", () => {
    if (ice.attrs.x + 32.5 >= 800 && ice.attrs.x + 32.5 <= 1450 && ice.attrs.y + 32.5 >= 10 && ice.attrs.y + 32.5 <= 650) {
        if (registeredComps.includes("Ice")) {
            var dx = (9 - 0) / (1417.5 - 767.5)
            var dy = (9 - 0) / (617.5 - (-22.5))
            var x = Math.round((Math.floor(ice.attrs.x) - 767.5) * dx)
            var y = Math.round((Math.floor(ice.attrs.y) - (-22.5)) * dy)
            ws.send(`CREATE_COMP ${mapId} Ice ${x} ${y}`)

            var newIce = new Konva.Image({
                x: 800 + x * 65 + 32.5,
                y: 10 + y * 65 + 32.5,
                width: 65,
                height: 65,
                offset: {
                    x: 32.5,
                    y: 32.5,
                },
            });
            newIce.on('mouseover', () => document.body.style.cursor = 'pointer')
            newIce.on('mouseout', () => document.body.style.cursor = 'default')
            layerObjects.add(newIce);
            var imageObj = new Image();
            imageObj.onload = function () {
                newIce.image(this)
            };
            imageObj.src = `./images/Ice.png`;
            newIce.on("click", () => {
                newIce.destroy()
                ws.send(`DELETE_COMP ${mapId} ${x} ${y}`)
            })
            newIce.on("wheel", () => {
                newIce.rotate(90)
                ws.send(`ROTATE_COMP ${mapId} ${x} ${y}`)
            })
        }
        else {
            notification.setAttr("text", "Component 'Ice' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    }
    ice.position({ x: 10, y: 520 })
})

var mud = new Konva.Image({
    x: 10,
    y: 600,
    width: 65,
    height: 65,
    draggable: true,
});
mud.on('mouseover', () => document.body.style.cursor = 'pointer')
mud.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(mud);
var imageObj = new Image();
imageObj.onload = function () {
    mud.image(this)
};
imageObj.src = `./images/Mud.png`;
mud.on("dragend", () => {
    if (mud.attrs.x + 32.5 >= 800 && mud.attrs.x + 32.5 <= 1450 && mud.attrs.y + 32.5 >= 10 && mud.attrs.y + 32.5 <= 650) {
        if (registeredComps.includes("Mud")) {
            var dx = (9 - 0) / (1417.5 - 767.5)
            var dy = (9 - 0) / (617.5 - (-22.5))
            var x = Math.round((Math.floor(mud.attrs.x) - 767.5) * dx)
            var y = Math.round((Math.floor(mud.attrs.y) - (-22.5)) * dy)
            ws.send(`CREATE_COMP ${mapId} Mud ${x} ${y}`)

            var newMud = new Konva.Image({
                x: 800 + x * 65 + 32.5,
                y: 10 + y * 65 + 32.5,
                width: 65,
                height: 65,
                offset: {
                    x: 32.5,
                    y: 32.5,
                },
            });
            newMud.on('mouseover', () => document.body.style.cursor = 'pointer')
            newMud.on('mouseout', () => document.body.style.cursor = 'default')
            layerObjects.add(newMud);
            var imageObj = new Image();
            imageObj.onload = function () {
                newMud.image(this)
            };
            imageObj.src = `./images/Mud.png`;
            newMud.on("click", () => {
                newMud.destroy()
                ws.send(`DELETE_COMP ${mapId} ${x} ${y}`)
            })
            newMud.on("wheel", () => {
                newMud.rotate(90)
                ws.send(`ROTATE_COMP ${mapId} ${x} ${y}`)
            })
        }
        else {
            notification.setAttr("text", "Component 'Mud' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    }
    mud.position({ x: 10, y: 600 })
})

var decoration = new Konva.Image({
    x: 10,
    y: 200,
    width: 65,
    height: 65,
    draggable: true,
});
decoration.on('mouseover', () => document.body.style.cursor = 'pointer')
decoration.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(decoration);
var imageObj = new Image();
imageObj.onload = function () {
    decoration.image(this)
};
imageObj.src = `./images/Decoration.png`;
decoration.on("dragend", () => {
    if (decoration.attrs.x + 32.5 >= 800 && decoration.attrs.x + 32.5 <= 1450 && decoration.attrs.y + 32.5 >= 10 && decoration.attrs.y + 32.5 <= 650) {
        if (registeredComps.includes("Decoration")) {
            var dx = (9 - 0) / (1417.5 - 767.5)
            var dy = (9 - 0) / (617.5 - (-22.5))
            var x = Math.round((Math.floor(decoration.attrs.x) - 767.5) * dx)
            var y = Math.round((Math.floor(decoration.attrs.y) - (-22.5)) * dy)
            ws.send(`CREATE_COMP ${mapId} Decoration ${x} ${y}`)

            var newDecoration = new Konva.Image({
                x: 800 + x * 65 + 32.5,
                y: 10 + y * 65 + 32.5,
                width: 65,
                height: 65,
                offset: {
                    x: 32.5,
                    y: 32.5,
                },
            });
            newDecoration.on('mouseover', () => document.body.style.cursor = 'pointer')
            newDecoration.on('mouseout', () => document.body.style.cursor = 'default')
            layerObjects.add(newDecoration);
            var imageObj = new Image();
            imageObj.onload = function () {
                newDecoration.image(this)
            };
            imageObj.src = `./images/Decoration.png`;
            newDecoration.on("click", () => {
                newDecoration.destroy()
                ws.send(`DELETE_COMP ${mapId} ${x} ${y}`)
            })
            newDecoration.on("wheel", () => {
                newDecoration.rotate(90)
                ws.send(`ROTATE_COMP ${mapId} ${x} ${y}`)
            })
        }
        else {
            notification.setAttr("text", "Component 'Decoration' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    }
    decoration.position({ x: 10, y: 200 })
})

// -------------- Handle car logic --------------
var porsche = new Konva.Image({
    x: 112.5,
    y: 460,
    width: 48,
    height: 25,
    draggable: true,
    offset: {
        x: 24,
        y: 12.5,
    },
});

porsche.on('mouseover', () => document.body.style.cursor = 'pointer')
porsche.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(porsche);
var imageObj = new Image();
imageObj.onload = function () {
    porsche.image(this)
};
imageObj.src = `./images/Porsche.png`;
porsche.on("dragend", () => {
    if (porsche.attrs.x + 24 >= 800 && porsche.attrs.x + 24 <= 1450 && porsche.attrs.y + 12.5 >= 10 && porsche.attrs.y + 12.5 <= 650) {
        if (registeredComps.includes("Car")) {
            ws.send(`CREATE_CAR ${mapId} Porsche BATUHAN 100 1000`)

            porsche.setAttr("x", 800 + 32.5)
            porsche.setAttr("y", 10 + 32.5)
            porsche.setAttr("draggable", false)
            porsche.moveToTop()

            porsche.on("click", () => {
                ws.send(`DELETE_CAR ${mapId} ${carIds[aliveCars.indexOf(porsche)]}`)
                if (activeCar == aliveCars.indexOf(porsche))
                    activeCar = -1
                aliveCars.splice(aliveCars.indexOf(porsche), 1)
                
                porsche.off("click")
                porsche.position({ x: 112.5, y: 460 })
                porsche.rotation(0)
                porsche.setAttr("draggable", true)
            })
            aliveCars.push(porsche)
        }
        else {
            porsche.position({ x: 112.5, y: 460 })

            notification.setAttr("text", "Component 'Car' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
        
    } else {
        porsche.position({ x: 112.5, y: 460 })
    }
})

var bmw = new Konva.Image({
    x: 112.5,
    y: 504,
    width: 48,
    height: 25,
    draggable: true,
    offset: {
        x: 24,
        y: 12.5,
    },
});
bmw.on('mouseover', () => document.body.style.cursor = 'pointer')
bmw.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(bmw);
var imageObj = new Image();
imageObj.onload = function () {
    bmw.image(this)
};
imageObj.src = `./images/Bmw.png`;
bmw.on("dragend", () => {
    if (bmw.attrs.x + 24 >= 800 && bmw.attrs.x + 24 <= 1450 && bmw.attrs.y + 12.5 >= 10 && bmw.attrs.y + 12.5 <= 650) {
        if (registeredComps.includes("Car")) {
            ws.send(`CREATE_CAR ${mapId} Bmw BATUHAN 80 1100`)

            bmw.setAttr("x", 800 + 32.5)
            bmw.setAttr("y", 10 + 32.5)
            bmw.setAttr("draggable", false)

            bmw.on("click", () => {
                ws.send(`DELETE_CAR ${mapId} ${carIds[aliveCars.indexOf(bmw)]}`)
                if (activeCar == aliveCars.indexOf(bmw))
                    activeCar = -1
                aliveCars.splice(aliveCars.indexOf(bmw), 1)
                
                bmw.off("click")
                bmw.position({ x: 112.5, y: 504 })
                bmw.rotation(0)
                bmw.setAttr("draggable", true)
            })
            aliveCars.push(bmw)
        }
        else {
            bmw.position({ x: 112.5, y: 504 })

            notification.setAttr("text", "Component 'Car' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    } else {
        bmw.position({ x: 112.5, y: 504 })
    }
})

var lambo = new Konva.Image({
    x: 112.5,
    y: 544,
    width: 48,
    height: 25,
    draggable: true,
    offset: {
        x: 24,
        y: 12.5,
    },
});
lambo.on('mouseover', () => document.body.style.cursor = 'pointer')
lambo.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(lambo);
var imageObj = new Image();
imageObj.onload = function () {
    lambo.image(this)
};
imageObj.src = `./images/Lamborghini.png`;
lambo.on("dragend", () => {
    if (lambo.attrs.x + 24 >= 800 && lambo.attrs.x + 24 <= 1450 && lambo.attrs.y + 12.5 >= 10 && lambo.attrs.y + 12.5 <= 650) {
        if (registeredComps.includes("Car")) {
            ws.send(`CREATE_CAR ${mapId} Lamborghini BATUHAN 110 800`)

            lambo.setAttr("x", 800 + 32.5)
            lambo.setAttr("y", 10 + 32.5)
            lambo.setAttr("draggable", false)

            lambo.on("click", () => {
                ws.send(`DELETE_CAR ${mapId} ${carIds[aliveCars.indexOf(lambo)]}`)
                if (activeCar == aliveCars.indexOf(lambo))
                    activeCar = -1
                aliveCars.splice(aliveCars.indexOf(lambo), 1)
                
                lambo.off("click")
                lambo.position({ x: 112.5, y: 544 })
                lambo.rotation(0)
                lambo.setAttr("draggable", true)
            })
            aliveCars.push(lambo)
        }
        else {
            lambo.position({ x: 112.5, y: 544 })

            notification.setAttr("text", "Component 'Car' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    } else {
        lambo.position({ x: 112.5, y: 544 })
    }
})

var ferr = new Konva.Image({
    x: 112.5,
    y: 584,
    width: 48,
    height: 25,
    draggable: true,
    offset: {
        x: 24,
        y: 12.5,
    },
});
ferr.on('mouseover', () => document.body.style.cursor = 'pointer')
ferr.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(ferr);
var imageObj = new Image();
imageObj.onload = function () {
    ferr.image(this)
};
imageObj.src = `./images/Ferrari.png`;
ferr.on("dragend", () => {
    if (ferr.attrs.x + 24 >= 800 && ferr.attrs.x + 24 <= 1450 && ferr.attrs.y + 12.5 >= 10 && ferr.attrs.y + 12.5 <= 650) {
        if (registeredComps.includes("Car")) {
            ws.send(`CREATE_CAR ${mapId} Ferrari BATUHAN 120 700`)

            ferr.setAttr("x", 800 + 32.5)
            ferr.setAttr("y", 10 + 32.5)
            ferr.setAttr("draggable", false)

            ferr.on("click", () => {
                ws.send(`DELETE_CAR ${mapId} ${carIds[aliveCars.indexOf(ferr)]}`)
                if (activeCar == aliveCars.indexOf(ferr))
                    activeCar = -1
                aliveCars.splice(aliveCars.indexOf(ferr), 1)

                ferr.off("click")
                ferr.position({ x: 112.5, y: 584 })
                ferr.rotation(0)
                ferr.setAttr("draggable", true)
            })
            aliveCars.push(ferr)
        }
        else {
            ferr.position({ x: 112.5, y: 584 })

            notification.setAttr("text", "Component 'Car' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    } else {
        ferr.position({ x: 112.5, y: 584 })
    }
})

var ford = new Konva.Image({
    x: 112.5,
    y: 624,
    width: 48,
    height: 25,
    draggable: true,
    offset: {
        x: 24,
        y: 12.5,
    },
});
ford.on('mouseover', () => document.body.style.cursor = 'pointer')
ford.on('mouseout', () => document.body.style.cursor = 'default')
layerObjects.add(ford);
var imageObj = new Image();
imageObj.onload = function () {
    ford.image(this)
};
imageObj.src = `./images/Ford.png`;
ford.on("dragend", () => {
    if (ford.attrs.x + 24 >= 800 && ford.attrs.x + 24 <= 1450 && ford.attrs.y + 12.5 >= 10 && ford.attrs.y + 12.5 <= 650) {
        if (registeredComps.includes("Car")) {
            ws.send(`CREATE_CAR ${mapId} Ford BATUHAN 70 1200`)

            ford.setAttr("x", 800 + 32.5)
            ford.setAttr("y", 10 + 32.5)
            ford.setAttr("draggable", false)

            ford.on("click", () => {
                ws.send(`DELETE_CAR ${mapId} ${carIds[aliveCars.indexOf(ford)]}`)
                if (activeCar == aliveCars.indexOf(ford))
                    activeCar = -1
                aliveCars.splice(aliveCars.indexOf(ford), 1)

                ford.off("click")
                ford.position({ x: 112.5, y: 624 })
                ford.rotation(0)
                ford.setAttr("draggable", true)
            })
            aliveCars.push(ford)
        }
        else {
            ford.position({ x: 112.5, y: 624 })

            notification.setAttr("text", "Component 'Car' is not registered.")
            clearTimeout(timerId)
            timerId = setTimeout(() => notification.setAttr("text", ""), 3000)
        }
    } else {
        ford.position({ x: 112.5, y: 624 })
    }
})

function toggleCar(carId) {
    if (carId < carIds.length) {
        if (activeCar !== carId) {
            activeCar = carId;
    
            for (i=0; i<carIds.length; i++) {
                if (i != carId)
                    ws.send(`STOP_CAR ${mapId} ${carIds[i]}`)
            }
    
            ws.send(`START_CAR ${mapId} ${carIds[carId]}`)
        } else {
            activeCar = -1
            ws.send(`STOP_CAR ${mapId} ${carIds[carId]}`)
        }
    }
}

function carAction(action) {
    if (activeCar >= 0 && activeCar <= 4) {
        ws.send(`${action}_CAR ${mapId} ${carIds[activeCar]}`)

        if (action === "LEFT") {
            aliveCars[activeCar].rotate(45)
        } else if (action === "RIGHT") {
            aliveCars[activeCar].rotate(-45)
        }
    }
}

var container = stage.container()
container.tabIndex = 1;
container.focus();
container.addEventListener("keydown", e => {
    switch (e.keyCode) {
        case 49: toggleCar(0); break;
        case 50: toggleCar(1); break;
        case 51: toggleCar(2); break;
        case 52: toggleCar(3); break;
        case 53: toggleCar(4); break;
        case 38: carAction("ACCEL"); break;
        case 40: carAction("BRAKE"); break;
        case 37: carAction("LEFT"); break;
        case 39: carAction("RIGHT"); break;
    }
})