// Method called to save CV to database
function saveChanges() {

  // Display loading bar
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

  // showApplicationLoadingModal('Success',JSON.stringify(cv));
  $.post('/applicant/save_cv', {cv: JSON.stringify(cv)}, function(data) {
    if (data == "Success") {
      showApplicationLoadingModal("Success","All Changes Saved");
    } else {
      // Data will be error message returned from server
      showApplicationLoadingModal("Failure",data);
    }
  });

}

// When the page loads, try and load a user's current CV
$(document).ready(function() {
  loadCV();
})
