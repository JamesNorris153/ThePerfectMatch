// Close the job modal
function closeJobModal() {
  $('#job_modal').removeClass('is-active');
}

// Show the job modal with data for a given/new job
function showJobModal(job_id) {

  // if job id is -1, this is a new job so use an empty template
  if (job_id == -1) {
    job_name = "";
    job_description = "";
    job_deadline = "";
    job_location = "";
    job_position = "Position";
    modal_title = "Add Job";
    job_status = "Available";
    job_question_number = "";
    job_questions = "[]";
  } else {
    // If not get all data from the table
    job_name = $('#'+job_id).find('.job_title').html();
    job_description = $('#'+job_id).find('.job_description').html();
    job_deadline = $('#'+job_id).find('.job_deadline').html();
    job_location = $('#'+job_id).find('.job_location').html();
    job_position = $('#'+job_id).find('.job_position').html();
    modal_title = "Edit Job";
    job_status = $('#'+job_id).find('.job_status').html();
    job_question_number = $('#'+job_id).find('.job_question_number').html();
    job_questions = $('#'+job_id).find('.job_questions').html();
  }

  // Display all job data in the modal
  $('#job_modal #cur_job_id').html(job_id);
  $('#job_modal .modal-card-title').html(modal_title);
  $('#job_modal input[name="job_name"]').val(job_name);
  $('#job_modal input[name="job_location"]').val(job_location);
  $('#job_modal input[name="job_deadline"]').val(job_deadline);
  $('#job_modal .job_description_box').val(job_description);
  $('#job_modal div[name="job_position"]').find('select').val(job_position);
  $('#job_modal div[name="job_status"]').find('select').val(job_status);
  $('#job_modal .question_number').val(job_question_number);

  // Delete any test questions left from last use
  $('.test_question:not(.template)').remove();

  // Get all questions and start adding them to the modal
  all_questions = JSON.parse(job_questions);
  for (i in all_questions) {
    question = all_questions[i];
    question_element = $('.add_question_button').parent().find(".template").clone().removeClass('template');
    question_title = question["Question"];
    correct = question["Correct"];
    incorrect1 = question["Incorrect1"];
    incorrect2 = question["Incorrect2"];
    incorrect3 = question["Incorrect3"];


    // Show the question and all answers
    $(question_element).find('input[name="question"]').val(question_title);
    $(question_element).find('input[name="correct_answer"]').val(correct);
    incorrect_inputs = $(question_element).find('input[name="incorrect_answer"]');
    $(incorrect_inputs[0]).val(incorrect1);
    $(incorrect_inputs[1]).val(incorrect2);
    $(incorrect_inputs[2]).val(incorrect3);

    // Insert the question at the end of the modal
    $(question_element).insertBefore('.add_question_button');
  }

  // Show the modal
  $('#job_modal').addClass('is-active');
}

// Close the completed job modal and job modal
function closeCompletedJobModal() {
  $('#saving_job_modal .modal-close').attr('onclick','closeJobLoadingModal();');
  closeJobLoadingModal();
  closeJobModal();
}

// Add functionality for the edit job button
$('#job_table').on('click', '.edit_button', function(event) {
  var job_id = $(this).parent().parent().parent().attr('id');
  showJobModal(job_id);
});

// Add functionality for the delete job button
$('#job_table').on('click', '.delete_button', function(event) {
    var job_id = $(this).parent().parent().parent().attr('id');
    // POST the job id for the job being delete to the database so that it can be deleted
    $.post("/staff/delete_job",{job_id:job_id},function(data) {
      if (data == "Success") {
        $('#'+job_id).remove();
      } else {
        alert(data);
      }
    });
});

function showRetrainModal(message) {
  $('#retrain_modal .modal-message').html(message);
  $('#retrain_modal').addClass('is-active');
}

function closeRetrainModal() {
  $('#retrain_modal').removeClass('is-active');
}

// Add functionality for the delete job button
$('#job_table').on('click', '.retrain_button', function(event) {
    var job_id = $(this).parent().parent().parent().attr('id');
    // POST the job id for the job being delete to the database so that it can be deleted
    $.post("/staff/retrain_job",{job_id:job_id},function(data) {
      if (data == "Success") {
        showRetrainModal("Retraining has begun for your job. You will receive an email to let you know when it is completed.");
      } else {
        showRetrainModal(data);
      }
    });
});

// Add functionality for the candidates button -> Redirect admin to a page of candidates for the selected job
$('#job_table').on('click', '.candidates_button', function(event) {
  var job_id = $(this).parent().parent().parent().attr('id');
  window.location.href="/staff/candidates?job_id="+job_id;
});


// Refresh all the jobs in the table
function refreshJobs() {

  // Get all jobs from the database
  $.get("/staff/get_jobs", function(data) {

    // If not logged in, redirect to landing page
    if (data == "You are not logged in") {
      window.location.href="/";
    }

    // Reset all data in  the table
    $('#job_table tbody .job:not(.template)').remove();

    // Get all jobs into a JSON object and start iteratin over them
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
      job_question_number = job["QuestionNumber"]
      job_questions = job["Questions"]

      // Insert all data into new row in table
      job_element = $(job_template).clone().removeClass('template').attr('id',job_id);
      $(job_element).find('.job_title').html(job_name);
      $(job_element).find('.job_location').html(job_location);
      $(job_element).find('.job_position').html(job_position);
      $(job_element).find('.job_deadline').html(job_deadline);
      $(job_element).find('.job_status').html(job_status);
      $(job_element).find('.job_description').html(job_description);
      $(job_element).find('.job_question_number').html(job_question_number);
      $(job_element).find('.job_questions').html(JSON.stringify(job_questions));


      // Insert job at top of table
      $(job_element).insertAfter($(job_template));
    }
  });
}

// When page loads, get all jobs into the table
$(document).ready(function() {
  refreshJobs();
});
