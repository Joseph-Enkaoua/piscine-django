$(document).ready(function() {
  function updatePage() {
    $.ajax({
      type: 'GET',
      url: statusUrl,
      success: function(response) {
        if (response.success && response.is_authenticated) {
          $('#login-section').hide();
          $('#logout-btn-navbar').show();
          $('#user-info').show();
          $('#logged-in-msg').text('Logged as ' + response.username);
        } else {
          $('#logout-btn-navbar').hide();
          $('#user-info').hide();
          $('#logged-in-msg').text('');
          $('#login-section').show();
        }
      },
      error: function() {
        $('#username').val('');
        $('#password').val('');
        $('#logout-btn-navbar').hide();
        $('#user-info').hide();
        $('#login-section').show();
      }
    });
  }

  $('#login-form').on('submit', function(event) {
    event.preventDefault();

    $('#form-errors').empty();

    $.ajax({
      type: 'POST',
      url: loginUrl,
      data: $(this).serialize(),
      success: function(response) {
        if (response.success) {
          $('#username').val('');
          $('#password').val('');
          updatePage();
        } else {
          $('#form-errors').html('Invalid username or password.');
        }
      },
      error() {
        $('#form-errors').html('An error occurred while trying to log in.');
      },
    });
  });

  $('#logout-btn').on('click', function() {
    $.ajax({
      type: 'POST',
      url: logoutUrl,
      success: function(response) {
        if (response.success) {
          updatePage();
        }
      },
      error: function() {
        $('#form-errors').html('An error occurred while trying to log out.');
      }
    });
  });

  updatePage();
});