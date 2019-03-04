// Save changes for the job being edited/added
function saveChanges() {

  // Show the saving modal
  $('#saving_job_modal').addClass('is-active');

  // Reset all errored out boxes
  $('.job_item:not(.template) .is-danger:not(.button)').removeClass('is-danger');

  // Null Input Checks (includes entering non-integer in years/months for employment)
  all_text_inputs = $('.job_item:not(.template) input:not(.button)');
  invalid_inputs = $(all_text_inputs).filter(function() { return $(this).val() == ""; });
  $(invalid_inputs).addClass('is-danger');
  invalid_selection_boxes = $('.job_item:not(.template) .select:has(option:selected.default_option)');
  $(invalid_selection_boxes).addClass('is-danger');
  if ($('.job_description_box').val() == "") {
    $('.job_description_box').addClass('is-danger');
  }

  // Get job properties
  job_name = $('#job_details input[name="job_name"]').val();
  job_position = $('#job_details div[name="job_position"] select option:selected').val();
  job_location = $('#job_details input[name="job_location"]').val();
  job_deadline = $('#job_details input[name="job_deadline"]').val();
  job_description = $('.job_description_box').val();

  // Error Check Deadline - Check it's a real date in the format DD/MM/YYYY
  var t = $('#job_details input[name="job_deadline"]').val().match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  if(t !== null){
    var d = +t[1], m = +t[2], y = +t[3];
    var date = new Date(y, m - 1, d);
    if(date.getFullYear() === y && date.getMonth() !== m - 1) {
      $('#job_details input[name="job_deadline"]').addClass('is-danger');
    }
  } else {
    $('#job_details input[name="job_deadline"]').addClass('is-danger');
  }

  // Get all the question elements
  all_questions = $('.test_question:not(.template)');

  // Get number of questions to randomly ask applicant - ensure it is a number between 0 and the number of questions entered
  question_number = $('.question_number').val();
  if (isNaN(question_number)) {
    $('.question_number').addClass('is-danger');
  } else if (question_number < 0 || question_number > $(all_questions).length) {
    $('.question_number').addClass('is-danger');
  }

  // If there have been any errors thus far, don't try parsing data
  if ($('.job_item:not(.template) .is-danger:not(.button)').length != 0) {
    showJobLoadingModal('Failure','Some details were not entered correctly, please see the red boxes');
    return;
  }

  // Get all questions in a JSON object
  question_details = []
  $(all_questions).each(function() {
    question = $(this).find('input[name="question"]').val();
    correct_answer = $(this).find('input[name="correct_answer"]').val();
    incorrect_answer_fields = $(this).find('input[name="incorrect_answer"]');
    incorrect_answers = []
    $(incorrect_answer_fields).each(function() {
      answer = $(this).val();
      incorrect_answers.push({
        "Answer":answer
      });
    });
    question_details.push({
      "Question":question,
      "Correct":correct_answer,
      "Incorrect":incorrect_answers
    });
  });

  // Get job status
  var job_status = $('#job_modal div[name="job_status"]').find('select').val();

  // Create job JSON object
  var job = {
    "Name":job_name,
    "Description":job_description,
    "Deadline":job_deadline,
    "Location":job_location,
    "Position":job_position,
    "Status":job_status,
    "Questions":question_details,
    "QuestionNumber":question_number
  };

  // If editing a job, get the current id for the job, otherwise it will be -1
  var job_id = $('#cur_job_id').html();

  // Send the job details to the API along with the job id
  $.post('/staff/save_job', {job_id:job_id, job: JSON.stringify(job)}, function(data) {
    // If successful, refresh all jobs
    if (data == "Success") {
      showJobLoadingModal("Success","All Changes Saved");
      refreshJobs();
      $(modal).find('.modal-background').attr('onclick','closeCompletedJobModal();');
      $(modal).find('.modal-close').attr('onclick','closeCompletedJobModal();');
    } else {
      // Data will be error message returned from server
      showJobLoadingModal("Failure",data);
    }
  });

}

// Delete a question in the test
function deleteItem(element) {
  $(element).parent().remove();
}

// Add a new test question
function addItem(element) {
  newItem = $(element).parent().find(".template").clone().removeClass('template');
  $(newItem).insertBefore(element);
}

// Close the loading modal and reset its data
function closeJobLoadingModal() {
  modal = $('#saving_job_modal');
  $(modal).removeClass('is-active');
  $(modal).find('.modal-close').addClass('is-hidden');
  $(modal).find('.progress').removeAttr('value').addClass('is-info').removeClass('is-success').removeClass('is-danger');
  $(modal).find('.modal-background').attr('onclick','');
  $(modal).find('.modal-message').html('LOADING...');
}

// Show the loading modal with a given state and message
function showJobLoadingModal(state,message) {
  modal = $('#saving_job_modal');
  if (state == "Success") {
    $(modal).find('.progress').removeClass('is-info').addClass('is-success');
  } else {
    $(modal).find('.progress').removeClass('is-info').addClass('is-danger');
  }
  $(modal).find('.modal-close').removeClass('is-hidden');
  $(modal).find('.progress').attr('value','100');
  $(modal).find('.modal-background').attr('onclick','closeJobLoadingModal();');
  $(modal).find('.modal-message').html(message);
}
