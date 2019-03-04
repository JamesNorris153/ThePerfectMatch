// Swap the user between the register and login forms
function swapForm() {
  $('.registerForm').toggleClass('is-hidden');
  $('.loginForm').toggleClass('is-hidden');
}

// Register new applicant - Return true/false on successful/unsuccessful registration
function register(fname_input,lname_input,email_input,password_input,confirm_password_input) {

  // Get user inputs
  first_name = $(fname_input).val();
  last_name = $(lname_input).val();
  email = $(email_input).val();
  password = $(password_input).val();
  confirm_password = $(confirm_password_input).val();

  // Check if first name has been entered
  if (first_name == "") {
    $(fname_input).addClass("is-danger");
  } else {
    $(fname_input).removeClass("is-danger");
  }

  // Check if last name has been entered
  if (last_name == "") {
    $(lname_input).addClass("is-danger");
  } else {
    $(lname_input).removeClass("is-danger");
  }

  // Check if email has been entered
  if (email == "") {
    $(email_input).addClass("is-danger");
  } else {
    $(email_input).removeClass("is-danger");
  }

  // Check if passwords have been entered and are the same
  if (password != confirm_password || password=="") {
    $(password_input).addClass("is-danger");
    $(confirm_password_input).addClass("is-danger");
    $('#register_error').html("Passwords do not match");
  } else {
    $(password_input).removeClass("is-danger");
    $(confirm_password_input).removeClass("is-danger");
  }

  // Check if any of the inputs have errors, stop processing if so
  if ($(fname_input).parent().find('.is-danger').length != 0) {
    return false;
  }

  // Send data to server to create user
  $.post("/applicant/register",
  {first_name:first_name, last_name:last_name, email:email, password:password},
   function(data) {
     // If user successfully created, send user to jobs page, else show the error message
     if (data == "Success") {
       window.location.href = "/applicant/jobs"
     } else {
       $('#register_error').html(data);
     }
  });

  // Prevent page reload
  return false;

}

// Register new applicant - Return true/false on successful/unsuccessful registration
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
  $.post("/applicant/login",
  {email:email, password:password},
   function(data) {
     // If user successfully logged in, send user to jobs page, else show the error message
     if (data == "Success") {
       window.location.href = "/applicant/jobs";
     } else {
       $('#login_error').html(data);
     }
  });

  // Prevent page reload
  return false;

}
