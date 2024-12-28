$(document).ready(function() {
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
});
