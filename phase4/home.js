var maps = []

const ws = new WebSocket("ws://localhost:8000");
ws.onopen = () => {
    ws.send("USER BATUHAN")
    ws.send("GET_ALL_MAPS")
}
var timerId
ws.onmessage = event => {
    const msg = event.data
    if (!(msg.includes("[") || msg.includes("Username set to"))) {
        var notification = document.getElementById("notification")
        notification.innerText = msg
        clearTimeout(timerId)
        timerId = setTimeout(() => notification.innerText = "", 3000)
    }

    if (msg.includes("[")) {
        maps = JSON.parse(msg)
        var list = document.getElementById("maps")
        list.innerHTML = ""
        maps.forEach(map => {
            var li = document.createElement("li")
            li.innerHTML = `<a href="javascript:selectMap(${map})">
                                Map ${map}
                            </a>
                            <button style="margin-left:10px" onclick="deleteMap(${map})">
                                Delete
                            </button>`
            list.append(li)
        })
    } else if (msg.includes("Map created with id") | msg.includes("was detached from all users and deleted.")) {
        ws.send("GET_ALL_MAPS")
    }
}

function selectMap(mapId) {
    document.location.href = `./game.html?map=${mapId}`
}

function createMap() {
    ws.send("CREATE_MAP 10 10 100 WHITE")
}

function deleteMap(mapId) {
    ws.send(`DELETE_MAP ${mapId}`)
}