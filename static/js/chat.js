$(function () {

    var url = `ws://${window.location.host}/ws/room/${room_id}/`
    var chatSocket = new WebSocket(url)

    chatSocket.onopen = function (e) {
        console.log('Websocket open')
    }
    chatSocket.onclose = function (e) {
        console.log('websocket close')
    }
    chatSocket.onmessage = function (data) {
        const datamsj = JSON.parse(data.data)
        var msj = datamsj.message
        var username = datamsj.username
        var datetime = datamsj.datetime

        document.querySelector('#boxMessages').innerHTML +=
            `
            <div class="alert alert-success" role="alert">
            ${msj}
                <div>
                    <small class="fst-italic fw-bold mt-2">${username}</small>
                    <small class="fst-italic fw-bold mt-2 float-end">${datetime}</small>
                </div>
            </div>
            `
    }
    console.log(url)
    document.querySelector('#btnMessage').addEventListener('click', sendMessage)
    document.querySelector('#inputMessage').addEventListener('keypress', function (e) {
        if (e.key == 'Enter') {
            sendMessage()
        }
    })

    function sendMessage() {
        var message = document.querySelector('#inputMessage')
        if (message.value.trim() != '') {
            loadMessageHTML(message.value.trim())
            chatSocket.send(JSON.stringify({
                message: message.value.trim(),
            }))

            console.log(message.value.trim())
            message.value = ''
        } else {
            console.log('no hay mensaje')
        }
    }

    function loadMessageHTML(m) {
        document.querySelector('#boxMessages').innerHTML +=
            `
            <div class="alert alert-primary" role="alert">
            ${m}
                <div>
                    <small class="fst-italic fw-bold mt-2">${user}</small>
                    <small class="fst-italic fw-bold mt-2 float-end">21-06-24</small>
                </div>
            </div>
            `
    }
})

