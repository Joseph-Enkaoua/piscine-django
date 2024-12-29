$(document).ready(function() {
  const socket = new WebSocket(wsUrl);

  // Event listener for connection open
  socket.addEventListener('open', (event) => {
    console.log('WebSocket connection opened')
  });

  // Event listener for receiving messages
  socket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "chat-message") {
      displayMessage(data);
    } else if (data.type === "chat-users") {
      $('#user-table').empty();
      data.list.forEach(element => {
        displayChatUsers(element);
      });
    }
  });

  // Event listener for connection close
  socket.addEventListener('close', (event) => {
      console.log('WebSocket connection closed');
  });

  // Event listener for connection errors
  socket.addEventListener('error', (event) => {
      console.error('WebSocket error:', event.error);
  });

  // Send button click event
  $('#send-button').click(() => {
    const messageInput = $('#message-input').val();
    if (messageInput.trim() !== '') {
      const payload = JSON.stringify({
        'message': messageInput,
      });
      socket.send(payload);
      $('#message-input').val('');
    }
  });

  function displayMessage(data) {
    const isCurrentUser = data.user === username;
    let messageClass = isCurrentUser ? 'current-user' : 'other-user';
    messageClass = data.user === 'system' ? 'system-message' : messageClass;

    const messageElement = `
      <div class="w-100 msg-area ${messageClass}">
        <p>${data.user}</p>
        <div class="message ${messageClass}">
          ${data.message}
        </div>
      </div>`;

    $('#chat-messages').append(messageElement);

    if (isCurrentUser || data.user === 'system') {
      $('#chat-messages p').last().remove();
    }

    $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);
  }

  function displayChatUsers(username) {
    $('#user-table').append(`<li class="list-group-item">${username}</li>`);
  }

  // Handle logout button
  $('#logout-btn').on('click', function() {
    $.ajax({
      type: 'POST',
      url: logoutUrl,
      success: function(response) {
        if (response.success) {
          window.location.href = loginUrl;
        }
      },
      error: function() {
        $('#form-errors').html('An error occurred while trying to log out.');
      }
    });
  });

  // Triger message send on Enter press
  $('#message-input').on('keyup', function(e) {
    if (e.key === 'Enter') {
        $('#send-button').click();
    }
  });

  $('#message-input').focus();
});
