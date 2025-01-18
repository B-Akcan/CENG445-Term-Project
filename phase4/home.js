var maps = []

const ws = new WebSocket("ws://localhost:8000");
ws.onopen = () => {
    ws.send("USER BATUHAN")
    ws.send("GET_ATTACHED_MAPS BATUHAN")
    ws.send("GET_UNATTACHED_MAPS BATUHAN")
}
var timerId
ws.onmessage = event => {
    const msg = event.data
    if (!(msg.startsWith("{") || msg.includes("Username set to"))) {
        var notification = document.getElementById("notification")
        notification.innerText = msg
        clearTimeout(timerId)
        timerId = setTimeout(() => notification.innerText = "", 3000)
    }

    if (msg.startsWith("{\"attached\":")) {
        maps = JSON.parse(msg).attached
        var list = document.getElementById("attached")
        list.innerHTML = ""
        maps.forEach(map => {
            var li = document.createElement("li")
            li.innerHTML = `<a href="javascript:selectMap(${map})">
                                Map ${map}
                            </a>
                            <button style="margin-left:10px" onclick="detachMap(${map})">
                                Detach
                            </button>
                            <button style="margin-left:10px" onclick="deleteMap(${map})">
                                Delete
                            </button>`
            list.append(li)
        })
    } else if (msg.startsWith("{\"unattached\":")) {
        maps = JSON.parse(msg).unattached
        var list = document.getElementById("unattached")
        list.innerHTML = ""
        maps.forEach(map => {
            var li = document.createElement("li")
            li.innerHTML = `Map ${map}
                            <button style="margin-left:10px" onclick="attachMap(${map})">
                                Attach
                            </button>`
            list.append(li)
        })
    } else {
        ws.send("GET_ATTACHED_MAPS BATUHAN")
        ws.send("GET_UNATTACHED_MAPS BATUHAN")
    }
}

function selectMap(mapId) {
    document.location.href = `./game.html?map=${mapId}`
}

function createMap() {
    ws.send("CREATE_MAP 10 10 100 WHITE")
}

function attachMap(mapId) {
    ws.send(`ATTACH_MAP ${mapId}`)
}

function detachMap(mapId) {
    ws.send(`DETACH_MAP ${mapId}`)
}

function deleteMap(mapId) {
    ws.send(`DELETE_MAP ${mapId}`)
}