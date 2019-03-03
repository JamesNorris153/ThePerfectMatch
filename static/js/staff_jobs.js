function closeJobModal() {
  $('#job_modal').removeClass('is-active');
}


function showJobModal(job_id) {

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

  $('#job_modal #cur_job_id').html(job_id);
  $('#job_modal .modal-card-title').html(modal_title);
  $('#job_modal input[name="job_name"]').val(job_name);
  $('#job_modal input[name="job_location"]').val(job_location);
  $('#job_modal input[name="job_deadline"]').val(job_deadline);
  $('#job_modal .job_description_box').html(job_description);
  $('#job_modal div[name="job_position"]').find('select').val(job_position);
  $('#job_modal div[name="job_status"]').find('select').val(job_status);
  $('#job_modal .question_number').val(job_question_number);

  $('.test_question:not(.template)').remove();

  all_questions = JSON.parse(job_questions);
  for (i in all_questions) {
    question = all_questions[i];
    question_element = $('.add_question_button').parent().find(".template").clone().removeClass('template');
    question_title = question["Question"];
    correct = question["Correct"];

    $(question_element).find('input[name="question"]').val(question_title);
    $(question_element).find('input[name="correct_answer"]').val(correct);

    incorrect_answers = question["Incorrect"];

    var i=0;
    $(question_element).find('input[name="incorrect_answer"]').each(function() {
      $(this).val(incorrect_answers[i]["Answer"]);
      i++;
    });

    $(question_element).insertBefore('.add_question_button');
  }

  $('#job_modal').addClass('is-active');
}


function closeCompletedJobModal() {
  $('#saving_job_modal .modal-close').attr('onclick','closeJobLoadingModal();');
  closeJobLoadingModal();
  closeJobModal();
}


$('#job_table').on('click', '.edit_button', function(event) {
  var job_id = $(this).parent().parent().parent().attr('id');
  showJobModal(job_id);
});


$('#job_table').on('click', '.delete_button', function(event) {
    var job_id = $(this).parent().parent().parent().attr('id');
    // DELETE JOB
    $.post("/staff/delete_job",{job_id:job_id},function(data) {
      if (data == "Success") {
        $('#'+job_id).remove();
      } else {
        alert(data);
      }
    });
});


$('#job_table').on('click', '.candidates_button', function(event) {
  var job_id = $(this).parent().parent().parent().attr('id');
  window.location.href="/staff/candidates?job_id="+job_id;
});


function refreshJobs() {

  $.get("/staff/get_jobs", function(data) {

    if (data == "You are not logged in") {
      window.location.href="/";
    }

    $('#job_table tbody .job:not(.template)').remove();


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
      job_question_number = 2; // TEMPORARY VALUE
      job_questions = [
        {"Question":"Q1",
        "Correct":"A",
        "Incorrect":[
          {"Answer":"B"},
          {"Answer":"C"},
          {"Answer":"D"}
        ]},
        {"Question":"Q2",
        "Correct":"A2",
        "Incorrect":[
          {"Answer":"B2"},
          {"Answer":"C2"},
          {"Answer":"D2"}
        ]}
      ]; // TEMPORARY VALUE

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


$(document).ready(function() {
  refreshJobs();
});
