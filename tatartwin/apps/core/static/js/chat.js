const MAX_LENGTH = 200

let detail_uri = window.location.href
let protocol = detail_uri.slice(0, detail_uri.indexOf(':'))
let WSPrefix = protocol[protocol.length-1] === 's' ? 's' : ''
let room_name = detail_uri.slice(detail_uri.lastIndexOf('/')+1)
let message_input = $('#chat-message-input')
let message_submit = $('#chat-message-submit')
let characters_left = $('#left')
let characters_max = $('#max')
let chat_log = $('#chat-log')

characters_left.text(message_input.val().length)
characters_max.text(MAX_LENGTH)
message_input.attr('maxlength', MAX_LENGTH)
chat_log.val('')

let chatSocket = new WebSocket(
    'ws' + WSPrefix + '://'
    + window.location.host
    + '/ws/chat/'
    + room_name
    + '/'
)

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    let current_log = chat_log.val()
    chat_log.val(current_log + data.message +'\n')
}

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly')
}

message_input.keyup(function(e) {
    let message = message_input.val()

    if(message.length <= MAX_LENGTH){
        characters_left.text(message.length)
    }else{
        characters_left.text(MAX_LENGTH)
    }

})

message_submit.click(function(e) {
    let message = message_input.val().trim()
    if (message.length > 0) {
        chatSocket.send(JSON.stringify({
            'message': message
        }))
        message_input.val('')
        characters_left.text(message_input.val().length)
    }
})
