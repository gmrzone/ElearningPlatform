
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + courseID
    + '/'
);
var mssginput = document.getElementById('chat-message-input');
var submitBtn = document.getElementById('chat-message-submit');

mssginput.focus()
mssginput.addEventListener('keyup', (e) => {
    if (e.which === 13){
        submitBtn.click()
    }
})

submitBtn.addEventListener('click', () => {
    let msg = mssginput.value
    if (msg){
        chatSocket.send(JSON.stringify({'message': msg}))
        mssginput.value = "";
        mssginput.focus()
    }

})

chatSocket.onmessage = function(e){
    let data = JSON.parse(e.data)
    let mssg = data['message']
    let chat_log = document.getElementById('chats')
    let name = data['username']
    let dateOptions = {hour: 'numeric', minute: 'numeric', hour12: true};
    let date =  new Date(data['time']).toLocaleString('en', dateOptions);
    let self = name === username ? true : false
    let name_span = document.createElement('span')
    let chatDiv = document.createElement('div')
    if (self){
        name_span.textContent = "Me";
        chatDiv.classList.add('chat')
        chatDiv.classList.add('self')
    }   
    else{
        name_span.textContent = name;
        chatDiv.className = 'chat'
    }
    name_span.className = 'name'
    let date_span = document.createElement('span')
    date_span.textContent = date
    date_span.className = 'date';
    let h3 = document.createElement('h3')
    h3.textContent = mssg;
    chatDiv.append(name_span, date_span, h3)
    
    chat_log.append(chatDiv)
    

}




chatSocket.onerror = (e) => {
    console.log("Unexpected Error occured")
}

