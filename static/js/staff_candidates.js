function showCVModal(candidate_id) {
  $.post("/staff/get_cv", {user_id:candidate_id}, function(data) {
    if (data == "Failure") {
      showErrorModal("There was an error retrieving this user's CV.<br>Please try again.");
    } else {
      $('#cv_modal').addClass('is-active');
    }
  });
}
function showErrorModal(message) {
  $('#error_modal').addClass('is-active').find('.modal-message').html(message);
}
function closeCVModal() {
  $('#cv_modal').removeClass('is-active');
}
$('#candidates_table').on('click', '.cv_button', function(event) {
  var candidate_id = $(this).parent().parent().parent().parent().attr('id');
  showCVModal(candidate_id);
});
