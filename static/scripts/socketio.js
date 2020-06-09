document.addEventListener('DOMContentLoaded', () => {
  var socket = io();

  let message;

  socket.on('message', data => {
    const p = document.createElement('p');
    const span_username = document.createElement('span');
    const span_timestamp = document.createElement('span');
    const br = document.createElement('br');
    span_username.innerHTML = data.username;
    span_timestamp.innerHTML = data.time_stamp;
    p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
    document.querySelector('#display-message-section').append(p);
  });


  document.querySelector('#send_message').onclick = () => {
    socket.send({'msg': document.querySelector('#user_message').value,
                  'username': username, 'message': message});
    // clear input area
    document.querySelector('#user_message').value = '';
  };

  document.querySelectorAll('.select-message').forEach(p => {
    p.onclick = () => {
      let newMessage = p.innerHTML;
      if (newMessage == message) {
        msg = `You are already in ${message} message.`
        printSysMsg(msg);
      } else {
        leaveMessage(message);
        joinMessage(newMessage);
        message = newMessage;
      }
    }
  });

  function leaveMessage(message) {
    socket.emit('leave', {'username': username, 'message': message});
  }

  function joinMessage(message) {
    socket.emit('join', {'username': username, 'message': message});
    // clear message
    document.querySelector('#display-message-section').innerHTML = ''
    // autofocus on text box
    document.querySelector('#user_message').focus();
  }

  function printSysMsg(msg) {
    const p = document.createElement('p');
    p.innerHTML = msg;
    document.querySelector('#display-message-section').append(p);
  }
});
