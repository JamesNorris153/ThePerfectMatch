function refreshCandidates() {
  $.get("/staff/get_candidates", function(data) {

    if (data == "You are not logged in") {
      window.location.href="/";
    } else if (data == "Could not find candidates for this job, please reload the page") {
      alert(data);
      return;
    } else if (data == "Could not retrieve data from the database") {
      alert("Could not retrieve data at this time, please try again");
      return;
    }

    $('#candidates_table tbody .candidate:not(.template)').remove();

    // candidates = JSON.parse(data);

    candidates = [
      {
  			"ID":"999232",
  			"First Name":"John",
  			"Last Name":"Smith",
  			"Email":"John.Smith@gmail.com",
  		 	"Score":1032,
  		 	"CVID":7824,
  		 	"Status":"Unknown"
      },
      {
  			"ID":"999233",
  			"First Name":"Fred",
  			"Last Name":"Estair",
  			"Email":"Fred@gmail.com",
  		 	"Score":542,
  		 	"CVID":60,
  		 	"Status":"Like"
      },
      {
  			"ID":"999234",
  			"First Name":"Jane",
  			"Last Name":"Doe",
  			"Email":"J.Doe@gmail.com",
  		 	"Score":750,
  		 	"CVID":12,
  		 	"Status":"Dislike"
      },
    ];
    candidate_template = $('.candidate.template');
    for (i in candidates) {

      candidate = candidates[i];
      candidate_id = candidate["ID"];
      candidate_name = candidate["First Name"]+" "+candidate["Last Name"];
      candidate_email = candidate["Email"];
      candidate_score = candidate["Score"];
      candidate_cv = candidate["CVID"];
      candidate_status = candidate["Status"];

      // Insert all data into new row in table
      candidate_element = $(candidate_template).clone().removeClass('template').attr('id',candidate_id);
      $(candidate_element).find('.candidate_name').html(candidate_name);
      $(candidate_element).find('.candidate_email').html(candidate_email);
      $(candidate_element).find('.candidate_score').html(candidate_score);
      $(candidate_element).find('.candidate_status').html(candidate_status);
      $(candidate_element).find('.cv_button').attr('onclick','showCVModal(this,'+candidate_cv+');');

      // Insert job at top of table
      $(candidate_element).insertAfter($(candidate_template));
    }
  });
}

$(document).ready(function() {
  refreshCandidates();
});

function showCVModal(element,cv_id) {

  $.post("/staff/get_cv",{cv_id:cv_id}, function(data) {

    if (data == "Failure") {
      showErrorModal("There was an error retrieving this user's CV.<br>Please try again.");
      return;
    }

    // Reset values
    $('.cv_item:not(.template):not(.university_item)').remove();
    $('.cv_item:not(.template) .is-danger:not(.button)').removeClass('is-danger');
    $('input[name="university_name"]').val("");
    $('input[name="degree_name"]').val("");
    $('input[name="degree_level"]').val("Level");

    cv = JSON.parse(data);

    fname = cv["FName"];
    lname = cv["LName"];
    degrees = cv["degrees"];
    languages = cv["languages"];
    hobbies = cv["hobbies"];
    alevels = cv["alevels"];
    employment = cv["employment"];
    skills = cv["skills"];

    university = degrees[0]["name"];
    course = degrees[0]["course"];
    grade = degrees[0]["grade"];
    $('input[name="university_name"]').val(university);
    $('input[name="degree_name"]').val(course);
    $('input[name="degree_level"]').val(grade);

    for (i in languages) {
      language = languages[i];
      name = language["name"];
      level = language["level"];

      new_language = $(".language.template").clone().removeClass('template');
      $(new_language).find('input[name="language_name"]').val(name);
      $(new_language).find('input[name="expertise"]').val(level);
      $(new_language).insertAfter('.language.template');

    }

    for (i in skills) {
      skill = skills[i];
      name = skill["name"];
      level = skill["level"];

      new_skill = $('.skill.template').clone().removeClass('template');
      $(new_skill).find('input[name="skill_name"]').val(name);
      $(new_skill).find('input[name="expertise"]').val(level);
      $(new_skill).insertBefore('.skill.template');

    }

    for (i in hobbies) {
      hobby = hobbies[i];
      name = hobby["name"];
      level = hobby["level"];

      new_hobby = $('.hobby.template').clone().removeClass('template');
      $(new_hobby).find('input[name="hobby_name"]').val(name);
      $(new_hobby).find('input[name="interest"]').val(level);
      $(new_hobby).insertBefore('.hobby.template');

    }

    for (i in alevels) {
      alevel = alevels[i];
      name = alevel["name"];
      level = alevel["level"];

      new_alevel = $('.a_level.template').clone().removeClass('template');
      $(new_alevel).find('input[name="subject_name"]').val(name);
      $(new_alevel).find('input[name="grade"]').val(level);
      $(new_alevel).insertBefore('.a_level.template');

    }

    for (i in employment) {
      job = employment[i];
      name = job["name"];
      position = job["position"];
      length = job["length"];

      new_job = $('.previous_employment.template').clone().removeClass('template');
      $(new_job).find('input[name="company_name"]').val(name);
      $(new_job).find('input[name="position_name"]').val(position);
      $(new_job).find('input[name="length"]').val(length);
      $(new_job).insertBefore('.previous_employment.template');

    }

    candidate_id = $(element).parent().parent().attr('id');
    candidate_status = $(element).parent().parent().find('.candidate_status').html();
    candidate_name = $(element).parent().parent().find('.candidate_name').html();
    candidate_email = $(element).parent().parent().find('.candidate_email').html();

    if (candidate_status == "Like") {
      $('.dislike_button').addClass('is-hidden').removeClass('is-danger').html('Dislike');
      $('.like_button').addClass('is-success').removeClass('is-hidden').html('Liked');
    } else if (candidate_status == "Dislike") {
      $('.like_button').addClass('is-hidden').removeClass('is-success').html('Like');
      $('.dislike_button').addClass('is-danger').removeClass('is-hidden').html('Disliked');
    } else {
      $('#cv_modal .like_button').attr('onclick','likeCandidate('+cv_id+','+candidate_id+',this);').removeClass('is-hidden is-success').html('Like');
      $('#cv_modal .dislike_button').attr('onclick','dislikeCandidate('+cv_id+','+candidate_id+',this);').removeClass('is-hidden is-danger').html('Dislike');
    }

    $('#cv_modal .modal-card-title').html(candidate_name+" - "+candidate_email);
    $('#cv_modal').addClass('is-active');
  });
}

function showErrorModal(message) {
  $('#error_modal').addClass('is-active').find('.modal-message').html(message);
}

function closeCVModal() {
  $('#cv_modal').removeClass('is-active');
}

function likeCandidate(cv_id,candidate_id,button) {
  $.post("/staff/like_candidate", {cv_id:cv_id}, function(data) {
    if (data == "Success") {
      $(button).attr('onclick','').html("Liked").addClass('is-success');
      $(button).parent().find('.dislike_button').addClass('is-hidden');
      $('#'+candidate_id).find('.candidate_status').html('Like');
    } else {
      alert(data);
    }
  });
}

function dislikeCandidate(cv_id,candidate_id,button) {
  $.post("/staff/dislike_candidate", {cv_id:cv_id}, function(data) {
    if (data == "Success") {
      $(button).attr('onclick','').html("Disliked").addClass('is-danger');
      $(button).parent().find('.like_button').addClass('is-hidden');
      $('#'+candidate_id).find('.candidate_status').html('Dislike');
    } else {
      alert(data);
    }
  });
}
