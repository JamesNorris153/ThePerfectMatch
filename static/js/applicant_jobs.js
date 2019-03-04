// Closes the description modal
function closeDescriptionModal() {
  $('#description_modal').removeClass('is-active');
}

// Shows the description modal and displays the description of the job selected
function showDescriptionModal(job_id) {
  description = $('#'+job_id).find('.job_description').html();
  $('#description_modal .modal-message').html(description);
  $('#description_modal').addClass('is-active');
}

// Closes the application modal
function closeApplicationModal() {
  $('#application_modal').removeClass('is-active');
}

// Loads the user's cv and shows it in the application modal
function showApplicationModal(job_id) {
  loadCV();
  $('#application_modal #cur_job_id').html(job_id);
  $('#application_modal').addClass('is-active');
}

// If the user successfully applies, this method will close both the application and it's loading modal
function closeCompletedApplicationModal() {
  $('#saving_cv_modal .modal-close').attr('onclick','closeApplicationLoadingModal();');
  closeApplicationLoadingModal();
  closeApplicationModal();
}

// Gets all data input by the user into their CV and uses a POST method to send it to the API
function saveChanges() {

  // Show the loading bar
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
    "Name": "NULL",
    "Degree Qualification": degree,
    "Degree Level": degree_level,
    "University Attended": university,
    "A-Level Qualifications": a_level_details,
    "Languages Known": language_details,
    "Previous Employment": employment_details,
    "Skills": skill_details,
    "Hobbies": hobby_details
  };

  // Get the id of the job being applied for
  var job_id = $('#cur_job_id').html();

  // Post the cv as a JSON string to the API
  $.post('/applicant/save_cv', {cv: JSON.stringify(cv)}, function(data) {

    // If the CV is successfully processed, apply the user for the job
    if (data == "Success") {
      // Post the id of the job being applied for
      $.post('/applicant/apply_for_job', {job_id:job_id}, function(data) {
        // Display whether the application was a success or failure, and let the user close either both or just the loading modal
        if (data == "Success") {
          showApplicationLoadingModal("Success","Your CV has been submitted.<br>In order to complete your application there will be a short test.<br>You can do this at any time by viewing the Jobs page.");
          $(modal).find('.modal-background').attr('onclick','closeCompletedApplicationModal();');
          $(modal).find('.modal-close').attr('onclick','closeCompletedApplicationModal();');
          $('#'+job_id+' .apply_button').addClass('is-hidden');
          $('#'+job_id+' .test_button').removeClass('is-hidden');
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

// Adds functionality to all apply buttons in the table
$('#job_table').on('click', '.apply_button', function(event) {
  var job_id = $(this).parent().parent().parent().attr('id');
  showApplicationModal(job_id);
});

// Adds functionality to all view(description) buttons in the table
$('#job_table').on('click', '.view_button', function(event) {
  var job_id = $(this).parent().parent().parent().attr('id');
  showDescriptionModal(job_id);
});

// Adds functionality to all test buttons in the table
$('#job_table').on('click', '.test_button', function(event) {
    var job_id = $(this).parent().parent().parent().attr('id');
    showTestModal(job_id);
});

// Adds functionality to all feedback buttons in the table
$('#job_table').on('click', '.feedback_button', function(event) {
    var job_id = $(this).parent().parent().parent().attr('id');
    showFeedbackModal(job_id);
});


// Shows the modal that allows applicants to take tests for the jobs they apply for
function showTestModal(job_id) {

  $.post("/applicant/get_job_test",{job_id:job_id},function(data) {
    questions = JSON.parse(data);

  // Reset the test modal
  $('.test_question:not(.template)').remove();

  // For each question being asked, get the question itself, and all the possible answers
  for (q in questions) {
    question = questions[q];
    question_name = question["Question"];
    answers = [];
    answers.push(question["Correct"]);
    answers.push(question["Incorrect1"]);
    answers.push(question["Incorrect2"]);
    answers.push(question["Incorrect3"]);

    // Create a new element for this question from the template
    test_question = $('.test_question.template').clone().removeClass('template');
    $(test_question).find('.question').html(question_name);

    // Shuffle and then display the answers
    for (var i = answers.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = answers[i];
        answers[i] = answers[j];
        answers[j] = temp;
    }
    $(test_question).find('.answer1').html(answers[0]);
    $(test_question).find('.answer2').html(answers[1]);
    $(test_question).find('.answer3').html(answers[2]);
    $(test_question).find('.answer4').html(answers[3]);

    // Label this question so that only one of the answers can be selected
    $(test_question).find('input[name="answer"]').attr('name',q);

    // Insert the question into the test area
    $(test_question).insertAfter($('.test_question.template'));

  }

  // Get information about the job and display it in the modal
  job_title = $('#'+job_id).find('.job_title').html();
  $('#test_modal .modal-card-title').html(job_title+" - Test");
  $('#cur_job_id').html(job_id);

  // Show the modal
  $('#test_modal').addClass('is-active');
});
}

// If the user gives up, close the test and show don't let them attempt it again
function giveUpTest() {
    job_id = $('#cur_job_id').html();
    $('#'+job_id).find('.test_button').addClass('is-hidden');
    $('#'+job_id).find('.feedback_button').removeClass('is-hidden');
    $('#test_modal').removeClass('is-active');
}

// Method for getting all the applicant's answers and sending them to the API
function submitTest() {

  // Get all the question elements from the test
  all_questions = $('.test_question:not(.template)');
  answers = [];

  // For each question, get the question itself and the answer the user gave
  $(all_questions).each(function(){
    question = $(this).find('.question').html();
    // If applicant hasn't selected an option, set answer to an empty string, otherwise get their answer
    if ($(this).find("input[type='radio']:checked").length == 0) {
      answer = "";
    } else {
      answer = $(this).find("input[type='radio']:checked").parent().find('span').html();
    }
    // Add the question and answer to the JSON object
    answers.push({
      "Question":question,
      "Answer":answer
    });
  });

  // Get the id of the job being tested for
  job_id = $('#cur_job_id').html();

  // Post the applicant's answers to the API and display the returned data
  $.post("/applicant/send_test_answers",{job_id:job_id,answers:JSON.stringify(answers)},function(data) {
    alert(data);
    if (data == "Success") {
      $('#test_feedback_modal').addClass('is-active');
      $('#'+job_id).find('.test_button').addClass('is-hidden');
      $('#'+job_id).find('.feedback_button').removeClass('is-hidden');
    } else {
      $('#test_error_modal .modal-message').html(data);
      $('#test_error_modal').addClass('is-active');
    }
  });

}

// Close both the feedback and test modals
function closeTestFeedbackModal() {
  $('#test_feedback_modal').removeClass('is-active');
  $('#test_modal').removeClass('is-active');
}

// Close the test error modal
function closeTestErrorModal() {
  $('#test_error_modal').removeClass('is-active');
}

// Close the feedback modal
function closeFeedbackModal() {
  $('#feedback_modal').removeClass('is-active');
}

// Show the feedback modal with the correct feedback according to how the recruiter judged the applicant's cv
function showFeedbackModal(job_id) {
  // Get the job title, and feedback level
  job_title = $('#'+job_id).find('.job_title').html();
  job_feedback = $('#'+job_id).find('.job_feedback').html();

  // Display the correct message for the right feedback level
  if (job_feedback == "0") {
    feedback = "Your application has been submitted and is with our hiring team. Once they have made a decision about your application, you will be notified via email.";
  } else if (job_feedback == "1") {
    feedback = "Unfortunately your application has not been selected for the next stage of hiring.";
  } else {
    feedback = "Your application has been selected by our staff for the next stage of hiring. A member of our team will be in contact with you via email soon.";
  }

  // Show the modal with the correct details
  $('#feedback_modal .modal-card-title').html(job_title);
  $('#feedback_modal .modal-card-body').html(feedback);
  $('#feedback_modal').addClass('is-active');
}

// Refresh the job table
function refreshJobs() {

  // Call the get_jobs method in the API
  $.get("/applicant/get_jobs", function(data) {

    // If user has been logged out somehow, redirect them to the login page
    if (data == "You are not logged in") {
      window.location.href="/";
    }

    // Remove all current data from the table
    $('#job_table tbody .job:not(.template)').remove();

    // Iterate over each job returned from the database
    job_template = $('.job.template');
    all_jobs = JSON.parse(data);
    for (i in all_jobs) {

      // Get all job data from JSON
      job = all_jobs[i];
      job_id = job["ID"];
      job_name = job["Name"];
      job_description = job["Description"];
      job_deadline = job["Deadline"];
      job_location = job["Location"];
      job_position = job["Position"];
      job_status = job["Status"];
      job_application = job["Application"];
      job_feedback = job["Feedback"];

      // Insert all data into new row in table
      job_element = $(job_template).clone().removeClass('template').attr('id',job_id);
      $(job_element).find('.job_title').html(job_name);
      $(job_element).find('.job_location').html(job_location);
      $(job_element).find('.job_position').html(job_position);
      $(job_element).find('.job_deadline').html(job_deadline);
      $(job_element).find('.job_status').html(job_status);
      $(job_element).find('.job_description').html(job_description);
      $(job_element).find('.job_feedback').html(job_feedback);

      // Check what stage of the application process they are in
      // 0 = Not Applied
      if (job_application == 0) {
        $(job_element).find('.apply_button').removeClass('is-hidden');
      }
      // 1 = Applied With CV but not taken test
      if (job_application == 1) {
        $(job_element).find('.test_button').removeClass('is-hidden');
      }
      // 2 = Applied with CV + Taken Test
      if (job_application == 2) {
        $(job_element).find('.feedback_button').removeClass('is-hidden');
      }

      // Insert job at top of table
      $(job_element).insertAfter($(job_template));
    }

  });
}

// When the page loads, get the jobs from the database
$(document).ready(function() {
  refreshJobs();
});
