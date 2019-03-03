function closeDescriptionModal() {
  $('#description_modal').removeClass('is-active');
}
function showDescriptionModal(job_id) {
  description = $('#'+job_id).find('.job_description').html();
  $('#description_modal .modal-message').html(description);
  $('#description_modal').addClass('is-active');
}

function closeApplicationModal() {
  $('#application_modal').removeClass('is-active');
}
function showApplicationModal(job_id) {
  loadCV();
  $('#application_modal #cur_job_id').html(job_id);
  $('#application_modal').addClass('is-active');
}
function closeCompletedApplicationModal() {
  $('#saving_cv_modal .modal-close').attr('onclick','closeApplicationLoadingModal();');
  closeApplicationLoadingModal();
  closeApplicationModal();
}

function closeTestModal() {
  $('#test_modal').removeClass('is-active');
}
function showTestModal(job_id) {
  $('#test_modal .modal-card-title').html("JOB:"+job_id);
  $('#test_modal #cur_job_id').html(job_id);
  $('#test_modal').addClass('is-active');
}
function submitTest() {
  $('#test_modal').removeClass('is-active');
  job_id = $('#cur_job_id').html();
  $('#'+job_id+' .test_button').removeClass('test_button').addClass('feedback_button').html("Feedback");
  closeTestModal();
}

function closeFeedbackModal() {
  $('#feedback_modal').removeClass('is-active');
}
function showFeedbackModal(job_id) {
  $('#feedback_modal .modal-card-title').html("JOB:"+job_id);
  $('#feedback_modal').addClass('is-active');
}

function saveChanges() {

  $('#saving_cv_modal').addClass('is-active');

  // Reset all errored out boxes
  $('.cv_item:not(.template) .is-danger:not(.button)').removeClass('is-danger');

  // Null Input Checks (includes entering non-integer in years/months for employment)
  all_text_inputs = $('.cv_item:not(.template) input:not(.button)');
  invalid_inputs = $(all_text_inputs).filter(function() { return $(this).val() == ""; });
  $(invalid_inputs).addClass('is-danger');
  invalid_selection_boxes = $('.cv_item:not(.template) .select:has(option:selected.default_option)');
  $(invalid_selection_boxes).addClass('is-danger');

  // If there have been any errors thus far, don't try parsing data
  if ($('.cv_item:not(.template) .is-danger:not(.button)').length != 0) {
    showApplicationLoadingModal('Failure','Some details were not entered correctly, please see the red boxes');
    return;
  }

  // Get university details
  university = $('#university_details input[name="university_name"]').val();
  degree = $('#university_details input[name="degree_name"]').val();
  degree_level = $('#university_details div[name="degree_level"] select option:selected').val();

  // Get all a-levels
  all_a_levels = $('.a_level:not(.template)');
  a_level_details = []
  $(all_a_levels).each(function() {
    subject_name = $(this).find('input[name="subject_name"]').val();
    grade = $(this).find('div[name="grade"] select option:selected').val();
    duplicate = false;
    for (each in a_level_details) {
      // If found in array, must be a duplicate
      if (a_level_details[each].Subject == subject_name) {
        duplicate = true;
      }
    }
    // If found to be a duplicate, mark it red
    if (duplicate) {
      $(this).find('input[name="subject_name"]').addClass('is-danger');
      $(this).find('div[name="grade"]').addClass('is-danger');
    } else {
      a_level_details.push({
        "Subject":subject_name,
        "Grade":grade
      });
    }
  });

  // Get all Languages
  all_languages = $('.language:not(.template)');
  language_details = []
  $(all_languages).each(function() {
    language_name = $(this).find('input[name="language_name"]').val();
    expertise = $(this).find('div[name="expertise"] select option:selected').val();
    duplicate = false;
    for (each in language_details) {
      // If found in array, must be a duplicate
      if (language_details[each].Language == language_name) {
        duplicate = true;
      }
    }
    // If found to be a duplicate, mark it red
    if (duplicate) {
      $(this).find('input[name="language_name"]').addClass('is-danger');
      $(this).find('div[name="expertise"]').addClass('is-danger');
    } else {
      language_details.push({
        "Language":language_name,
        "Expertise":expertise
      });
    }
  });

  // Get all Employment
  all_employment = $('.previous_employment:not(.template)');
  employment_details = []
  $(all_employment).each(function() {
    company_name = $(this).find('input[name="company_name"]').val();
    position_name = $(this).find('input[name="position_name"]').val();
    years = $(this).find('input[name="years"]').val();
    months = $(this).find('input[name="months"]').val();
    employment_length = years+" years "+months+" months";
    duplicate = false;
    for (each in employment_details) {
      // If found in array, must be a duplicate
      if (employment_details[each].Company == company_name && employment_details[each].Position == position_name) {
        duplicate = true;
      }
    }
    // If found to be a duplicate, mark it red
    if (duplicate) {
      $(this).find('input[name="company_name"]').addClass('is-danger');
      $(this).find('input[name="position_name"]').addClass('is-danger');
      $(this).find('input[name="years"]').addClass('is-danger');
      $(this).find('input[name="months"]').addClass('is-danger');
    } else {
      employment_details.push({
        "Company":company_name,
        "Position":position_name,
        "Length of Employment":employment_length
      });
    }
  });

  // Get all Skills
  all_skills = $('.skill:not(.template)');
  skill_details = []
  $(all_skills).each(function() {
    skill_name = $(this).find('input[name="skill_name"]').val();
    expertise = $(this).find('div[name="expertise"] select option:selected').val();
    duplicate = false;
    for (each in skill_details) {
      // If found in array, must be a duplicate
      if (skill_details[each].Skill == skill_name) {
        duplicate = true;
      }
    }
    // If found to be a duplicate, mark it red
    if (duplicate) {
      $(this).find('input[name="skill_name"]').addClass('is-danger');
      $(this).find('div[name="expertise"]').addClass('is-danger');
    } else {
      skill_details.push({
        "Skill":skill_name,
        "Expertise":expertise
      });
    }
  });

  // Get all Hobbies
  all_hobbies = $('.hobby:not(.template)');
  hobby_details = []
  $(all_hobbies).each(function() {
    hobby_name = $(this).find('input[name="hobby_name"]').val();
    interest = $(this).find('div[name="interest"] select option:selected').val();
    duplicate = false;
    for (each in hobby_details) {
      // If found in array, must be a duplicate
      if (hobby_details[each].Name == hobby_name) {
        duplicate = true;
      }
    }
    // If found to be a duplicate, mark it red
    if (duplicate) {
      $(this).find('input[name="hobby_name"]').addClass('is-danger');
      $(this).find('div[name="interest"]').addClass('is-danger');
    } else {
      hobby_details.push({
        "Name":hobby_name,
        "Interest":interest
      });
    }
  });

  // If some inputs were invalid, don't try create a cv
  if ($('.cv_item:not(.template) .is-danger:not(.button)').length != 0) {
    showApplicationLoadingModal('Failure','Some inputted values were duplicates, please see the red boxes');
    return;
  }

  // Create JSON CV
  var cv = {
    // NEED TO GET USER'S NAME FROM SOMEWHERE
    "Name": "NAMETY NAME",
    "Degree Qualification": degree,
    "Degree Level": degree_level,
    "University Attended": university,
    "A-Level Qualifications": a_level_details,
    "Languages Known": language_details,
    "Previous Employment": employment_details,
    "Skills": skill_details,
    "Hobbies": hobby_details
  };

  var job_id = $('#cur_job_id').html();

  $.post('/applicant/save_cv', {cv: JSON.stringify(cv)}, function(data) {
    if (data == "Success") {
      $.post('/applicant/apply_for_job', {job_id:job_id}, function(data) {
        if (data == "Success") {
          showApplicationLoadingModal("Success","Your CV has been submitted.<br>In order to complete your application there will be a short test.<br>You can do this at any time by viewing the Jobs page.");
          $(modal).find('.modal-background').attr('onclick','closeCompletedApplicationModal();');
          $(modal).find('.modal-close').attr('onclick','closeCompletedApplicationModal();');
          $('#'+job_id+' .apply_button').removeClass('apply_button').addClass('test_button').html("Test");
        } else {
          showApplicationLoadingModal("Failure",data);
        }
      });
    } else {
      // Data will be error message returned from server
      showApplicationLoadingModal("Failure",data);
    }
  });

}
$('#job_table').on('click', '.apply_button', function(event) {
  var job_id = $(this).parent().parent().parent().attr('id');
  showApplicationModal(job_id);
});
$('#job_table').on('click', '.view_button', function(event) {
  var job_id = $(this).parent().parent().parent().attr('id');
  showDescriptionModal(job_id);
});
$('#job_table').on('click', '.test_button', function(event) {
    var job_id = $(this).parent().parent().parent().attr('id');
    showTestModal(job_id);
});
$('#job_table').on('click', '.feedback_button', function(event) {
    var job_id = $(this).parent().parent().parent().attr('id');
    showFeedbackModal(job_id);
});
