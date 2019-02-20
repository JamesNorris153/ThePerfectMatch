function showCVModal(candidate_id,job_id) {
  $.post("/staff/get_cv", {user_id:candidate_id, job_id:job_id}, function(data) {
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
  var candidate_id = $(this).parent().parent().parent().parent().find('.applied_candidate_name').attr('value');
  var job_id = $(this).parent().parent().parent().parent().find('.applied_job_title').attr('value');
  showCVModal(candidate_id, job_id);
});

$('#candidates_table').on('click', '.like_button', function(event) {
  var clicked_button = $(this);
  var candidate_id = $(this).parent().parent().parent().parent().find('.applied_candidate_name').attr('value');
  var job_id = $(this).parent().parent().parent().parent().find('.applied_job_title').attr('value');
  $.post("/staff/like_candidate", {candidate_id:candidate_id, job_id:job_id}, function(data) {
    if (data == "Success") {
      $(clicked_button).removeClass('like_button').html("Liked").addClass('is-success');
      $(clicked_button).parent().parent().find('.dislike_button').parent().remove();
    } else {
      alert(data);
    }
  });
});

$('#candidates_table').on('click', '.dislike_button', function(event) {
  var clicked_button = $(this);
  var candidate_id = $(this).parent().parent().parent().parent().find('.applied_candidate_name').attr('value');
  var job_id = $(this).parent().parent().parent().parent().find('.applied_job_title').attr('value');
  $.post("/staff/dislike_candidate", {candidate_id:candidate_id, job_id:job_id}, function(data) {
    if (data == "Success") {
      $(clicked_button).removeClass('dislike_button').html("Disliked").addClass('is-danger');
      $(clicked_button).parent().parent().find('.like_button').parent().remove();
    } else {
      alert(data);
    }
  });
});
