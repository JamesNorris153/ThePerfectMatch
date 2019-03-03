function deleteItem(element) {
  $(element).parent().parent().parent().remove();
}
function addItem(element) {
  newItem = $(element).parent().find(".template").clone().removeClass('template');
  $(newItem).insertBefore(element);
}
function closeApplicationLoadingModal() {
  modal = $('#saving_cv_modal');
  $(modal).removeClass('is-active');
  $(modal).find('.modal-close').addClass('is-hidden');
  $(modal).find('.progress').removeAttr('value').addClass('is-info').removeClass('is-success').removeClass('is-danger');
  $(modal).find('.modal-background').attr('onclick','');
  $(modal).find('.modal-message').html('LOADING...');
}
function showApplicationLoadingModal(state,message) {
  modal = $('#saving_cv_modal');
  if (state == "Success") {
    $(modal).find('.progress').removeClass('is-info').addClass('is-success');
  } else {
    $(modal).find('.progress').removeClass('is-info').addClass('is-danger');
  }
  $(modal).find('.modal-close').removeClass('is-hidden');
  $(modal).find('.progress').attr('value','100');
  $(modal).find('.modal-background').attr('onclick','closeApplicationLoadingModal();');
  $(modal).find('.modal-message').html(message);
}
function loadCV() {
  $.get("/applicant/get_cv",function(data) {

    // Reset values
    $('.cv_item:not(.template):not(.university_item)').remove();
    $('.cv_item:not(.template) .is-danger:not(.button)').removeClass('is-danger');
    $('input[name="university_name"]').val("");
    $('input[name="degree_name"]').val("");
    $('div[name="degree_level"] select').val("Level");

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
    $('div[name="degree_level"] select').val(grade);

    for (i in languages) {
      language = languages[i];
      name = language["name"];
      level = language["level"];

      new_language = $('.add_language_button').parent().find(".template").clone().removeClass('template');
      $(new_language).find('input[name="language_name"]').val(name);
      $(new_language).find('div[name="expertise"] select').val(level);
      $(new_language).insertBefore('.add_language_button');

    }

    for (i in skills) {
      skill = skills[i];
      name = skill["name"];
      level = skill["level"];

      new_skill = $('.add_skill_button').parent().find(".template").clone().removeClass('template');
      $(new_skill).find('input[name="skill_name"]').val(name);
      $(new_skill).find('div[name="expertise"] select').val(level);
      $(new_skill).insertBefore('.add_skill_button');

    }

    for (i in hobbies) {
      hobby = hobbies[i];
      name = hobby["name"];
      level = hobby["level"];

      new_hobby = $('.add_hobby_button').parent().find(".template").clone().removeClass('template');
      $(new_hobby).find('input[name="hobby_name"]').val(name);
      $(new_hobby).find('div[name="interest"] select').val(level);
      $(new_hobby).insertBefore('.add_hobby_button');

    }

    for (i in alevels) {
      alevel = alevels[i];
      name = alevel["name"];
      level = alevel["level"];

      new_alevel = $('.add_a_level_button').parent().find(".template").clone().removeClass('template');
      $(new_alevel).find('input[name="subject_name"]').val(name);
      $(new_alevel).find('div[name="grade"] select').val(level);
      $(new_alevel).insertBefore('.add_a_level_button');

    }

    for (i in employment) {
      job = employment[i];
      name = job["name"];
      position = job["position"];
      length = job["length"];

      var numbers = length.match(/\d+/g).map(Number);
      years = numbers[0];
      months = numbers[1];

      new_job = $('.add_employment_button').parent().find(".template").clone().removeClass('template');
      $(new_job).find('input[name="company_name"]').val(name);
      $(new_job).find('input[name="position_name"]').val(position);
      $(new_job).find('input[name="years"]').val(years);
      $(new_job).find('input[name="months"]').val(months);
      $(new_job).insertBefore('.add_employment_button');

    }

  });
}
