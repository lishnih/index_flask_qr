// stan 2018-08-05


function update_user_section() {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: 'logged',
    success: function(data) {
      console.log(data);

      if (data.result == 'error') {
        $('#info').html(data.message);
        $('#InfoModal').modal('toggle');
      } else {
        if (data.is_anonymous) {
          $('#user_section').hide();
          $('#anonymous_section').show();
        } else {
          $('#anonymous_section').hide();
          $('#user_section').show();
        }
      }
    },
    error: function(data) {
//    $('#debug').html(data.responseText);
      $('#info').html("Some server issues on request!<br />\n'{0}'".format(data.statusText));
      $('#InfoModal').modal('toggle');
    },
  });
} // update_user_section
