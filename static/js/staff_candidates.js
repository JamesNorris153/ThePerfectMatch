// Method to refresh the candidates table data
function refreshCandidates() {

  job_id = $('#job_id').html();

  // Make get call to API to get all candidates for the current job
  $.post("/staff/get_candidates",{job_id:job_id}, function(data) {

    // If not logged in, redirect, and if error, display to user
    if (data == "You are not logged in") {
      window.location.href="/";
    } else if (data == "Could not find candidates for this job, please reload the page") {
      alert(data);
    } else if (data == "Could not retrieve data from the database") {
      alert("Could not retrieve data at this time, please try again");
    } else if (data == null) {
      $('#total_applicants').html(0);
      $('#liked_applicants').html(0);
      $('#disliked_applicants').html(0);
      $('#unknown_applicants').html(0);
    } else {
      // Reset the table
      $('#candidates_table tbody .candidate:not(.template)').remove();

      candidates = data;

      // Iterate over each received candidate and add them to the table
      candidate_template = $('.candidate.template');
      for (i in candidates) {

        // Get the candidate's data
        candidate = candidates[i];
        candidate_id = candidate["ID"];
        candidate_name = candidate["First Name"]+" "+candidate["Last Name"];
        candidate_email = candidate["Email"];
        candidate_score = parseInt(i)+1;
        candidate_cv = candidate["CVID"];
        if (candidate["Status"] == 0) {
          candidate_status = "Unknown";
        } else if (candidate["Status"] == 1) {
          candidate_status = "Like";
        } else {
          candidate_status = "Dislike";
        }

        // Insert all data into new row in table
        candidate_element = $(candidate_template).clone().removeClass('template').attr('id',candidate_id);
        $(candidate_element).find('.candidate_name').html(candidate_name);
        $(candidate_element).find('.candidate_email').html(candidate_email);
        $(candidate_element).find('.candidate_score').html(candidate_score);
        $(candidate_element).find('.candidate_status').html(candidate_status);
        $(candidate_element).find('.cv_button').attr('onclick','showCVModal(this,'+candidate_cv+');');

        // Insert job at top of table
        $(candidate_element).insertAfter($('.candidate:last-of-type'));
      }

      // Get applicant statistics and display them in the top bar
      applicant_number = candidates.length;
      liked_applicant_number = $('.candidate_status:contains("Like")').length;
      disliked_applicant_number = $('.candidate_status:contains("Dislike")').length;
      unknown_applicant_number = $('.candidate_status:contains("Unknown")').length;
      $('#total_applicants').html(applicant_number);
      $('#liked_applicants').html(liked_applicant_number);
      $('#disliked_applicants').html(disliked_applicant_number);
      $('#unknown_applicants').html(unknown_applicant_number);
    }

  });
}

// When the page loads, get all candidates
$(document).ready(function() {
  refreshCandidates();
});

// Show the CV Modal which contains the CV of the selected candidate
function showCVModal(element,cv_id) {

  // Use POST call to get selected CV from database
  $.post("/staff/get_cv",{cv_id:cv_id}, function(data) {

    // If there was an error getting the data, display the rror
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

    // Parse the cv into a JSON object
    cv = JSON.parse(data);

    // Get the cv attributes from the JSON object
    fname = cv["FName"];
    lname = cv["LName"];
    degrees = cv["degrees"];
    languages = cv["languages"];
    hobbies = cv["hobbies"];
    alevels = cv["alevels"];
    employment = cv["employment"];
    skills = cv["skills"];

    // Display university details
    university = degrees[0]["name"];
    course = degrees[0]["course"];
    grade = degrees[0]["grade"];
    $('input[name="university_name"]').val(university);
    $('input[name="degree_name"]').val(course);
    $('input[name="degree_level"]').val(grade);

    // Display language details
    for (i in languages) {
      language = languages[i];
      name = language["name"];
      level = language["level"];

      new_language = $(".language.template").clone().removeClass('template');
      $(new_language).find('input[name="language_name"]').val(name);
      $(new_language).find('input[name="expertise"]').val(level);
      $(new_language).insertAfter('.language.template');
    }

    // Display skill details
    for (i in skills) {
      skill = skills[i];
      name = skill["name"];
      level = skill["level"];

      new_skill = $('.skill.template').clone().removeClass('template');
      $(new_skill).find('input[name="skill_name"]').val(name);
      $(new_skill).find('input[name="expertise"]').val(level);
      $(new_skill).insertBefore('.skill.template');
    }

    // Display hobby details
    for (i in hobbies) {
      hobby = hobbies[i];
      name = hobby["name"];
      level = hobby["level"];

      new_hobby = $('.hobby.template').clone().removeClass('template');
      $(new_hobby).find('input[name="hobby_name"]').val(name);
      $(new_hobby).find('input[name="interest"]').val(level);
      $(new_hobby).insertBefore('.hobby.template');
    }

    // Display alevel details
    for (i in alevels) {
      alevel = alevels[i];
      name = alevel["name"];
      level = alevel["level"];

      new_alevel = $('.a_level.template').clone().removeClass('template');
      $(new_alevel).find('input[name="subject_name"]').val(name);
      $(new_alevel).find('input[name="grade"]').val(level);
      $(new_alevel).insertBefore('.a_level.template');
    }

    // Display employment details
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

    // Get candidate details from the table
    candidate_id = $(element).parent().parent().attr('id');
    candidate_status = $(element).parent().parent().find('.candidate_status').html();
    candidate_name = $(element).parent().parent().find('.candidate_name').html();
    candidate_email = $(element).parent().parent().find('.candidate_email').html();

    // Display the correct Like/Dislike buttons from the candidate_status
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

    // Set the card title to the candidates name and email, then show the modal
    $('#cv_modal .modal-card-title').html(candidate_name+" - "+candidate_email);
    $('#cv_modal').addClass('is-active');
  });
}

// Show the error modal with a given message
function showErrorModal(message) {
  $('#error_modal').addClass('is-active').find('.modal-message').html(message);
}

// Close the CV mdodal
function closeCVModal() {
  $('#cv_modal').removeClass('is-active');
}

// Like a candidate given their cv and candidate id's
function likeCandidate(cv_id,candidate_id,button) {
  // Send the like for the cv to the database so that it can be used in ML
  job_id = $('#job_id').html();
  $.post("/staff/like_candidate", {cv_id:cv_id,job_id:job_id}, function(data) {
    if (data == "Success") {
      // Don't let the admin like the same person again
      $(button).attr('onclick','').html("Liked").addClass('is-success');
      $(button).parent().find('.dislike_button').addClass('is-hidden');
      $('#'+candidate_id).find('.candidate_status').html('Like');

      // Update the applicant stats
      unknown_applicant_number = Number($('#unknown_applicants').html());
      liked_applicant_number = Number($('#liked_applicants').html());
      $('#liked_applicants').html(liked_applicant_number+1);
      $('#unknown_applicants').html(unknown_applicant_number-1);
    } else {
      alert(data);
    }
  });
}

// Dislike a candidate given their cv and candidate id's
function dislikeCandidate(cv_id,candidate_id,button) {
  job_id = $('#job_id').html();
  // Send the dislike for the cv to the database so that it can be used in ML
  $.post("/staff/dislike_candidate", {cv_id:cv_id,job_id:job_id}, function(data) {
    if (data == "Success") {
      // Don't let the admin dislike the same person again
      $(button).attr('onclick','').html("Disliked").addClass('is-danger');
      $(button).parent().find('.like_button').addClass('is-hidden');
      $('#'+candidate_id).find('.candidate_status').html('Dislike');

      // Update the applicant stats
      unknown_applicant_number = Number($('#unknown_applicants').html());
      disliked_applicant_number = Number($('#disliked_applicants').html());
      $('#disliked_applicants').html(disliked_applicant_number+1);
      $('#unknown_applicants').html(unknown_applicant_number-1);
    } else {
      alert(data);
    }
  });
}
