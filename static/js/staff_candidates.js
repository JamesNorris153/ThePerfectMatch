function showCVModal(candidate_id,job_id) {
  $.post("/staff/get_cv", {user_id:candidate_id, job_id:job_id}, function(data) {
    if (data == "Failure") {
      showErrorModal("There was an error retrieving this user's CV.<br>Please try again.");
    } else {
      $('#cv_modal .like_button').attr('onclick','likeCandidate('+candidate_id+','+job_id+',this);').removeClass('is-hidden is-success').html('Like');
      $('#cv_modal .dislike_button').attr('onclick','dislikeCandidate('+candidate_id+','+job_id+',this);').removeClass('is-hidden is-danger').html('Dislike');
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

function likeCandidate(candidate_id,job_id,button) {
  $.post("/staff/like_candidate", {candidate_id:candidate_id, job_id:job_id}, function(data) {
    if (data == "Success") {
      $(button).attr('onclick','').html("Liked").addClass('is-success');
      $(button).parent().find('.dislike_button').addClass('is-hidden');
    } else {
      alert(data);
    }
  });
}

function dislikeCandidate(candidate_id,job_id,button) {
  $.post("/staff/dislike_candidate", {candidate_id:candidate_id, job_id:job_id}, function(data) {
    if (data == "Success") {
      $(button).attr('onclick','').html("Disliked").addClass('is-danger');
      $(button).parent().find('.like_button').addClass('is-hidden');
    } else {
      alert(data);
    }
  });
}

$('#candidates_table').on('click', '.cv_button', function(event) {
  var candidate_id = $(this).parent().parent().parent().parent().find('.applied_candidate_name').attr('value');
  var job_id = $(this).parent().parent().parent().parent().find('.applied_job_title').attr('value');
  showCVModal(candidate_id, job_id);
});
