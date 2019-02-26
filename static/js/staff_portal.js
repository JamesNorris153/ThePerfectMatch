// Login staff member
function login(email_input,password_input) {

  // Get user inputs
  email = $(email_input).val();
  password = $(password_input).val();

  // Check if email has been entered
  if (email == "") {
    $(email_input).addClass("is-danger");
  } else {
    $(email_input).removeClass("is-danger");
  }

  // Check if password has been entered
  if (password == "") {
    $(password_input).addClass("is-danger");
  } else {
    $(password_input).removeClass("is-danger");
  }

  // Check if any of the inputs have errors, stop processing if so
  if ($(email_input).parent().find('.is-danger').length != 0) {
    return false;
  }

  // Send data to server to create user
  $.post("/staff/login",
  {email:email, password:password},
  function(data) {
    // If user successfully logged in, send user to candidates page, else show the error message
    if (data == "Success") {
      window.location.href = "/staff/jobs";
    } else {
      $('#login_error').html(data);
    }
  });

  // Prevent page reload
  return false;

}
