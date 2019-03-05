// Change the user's password in the database
function changePassword(old_input,new_input,confirm_input) {
  $('#change_error').removeClass('has-text-success').removeClass('has-text-danger').html('');
  old = $(old_input).val();
  new_pass = $(new_input).val();
  confirm = $(confirm_input).val();

  if (old == "") {
    $(old_input).addClass('is-danger');
  } else {
    $(old_input).removeClass('is-danger');
  }

  if (new_pass != confirm || new_pass == "" || confirm == "") {
    $(new_input).addClass('is-danger');
    $(confirm_input).addClass('is-danger');
    $('#change_error').html('New password must not be empty, and must be confirmed').addClass('has-text-danger');
  } else {
    $(new_input).removeClass('is-danger');
    $(confirm_input).removeClass('is-danger');
  }

  if ($(old_input).hasClass('is-danger') || $(new_input).hasClass('is-danger') || $(confirm_input).hasClass('is-danger')) {
    return false;
  }

  $.post("/staff/change_password",{current_password:old,new_password:new_pass},function(data) {
    if (data == "Success") {
      $(old_input).val('');
      $(new_input).val('');
      $(confirm_input).val('');
      $('#change_error').html('Your password has been successfully changed').addClass('has-text-success');
    } else {
      $('#change_error').html(data).addClass('has-text-danger');
    }
  });

  // Prevent page reload
  return false;
}
