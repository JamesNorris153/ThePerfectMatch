function toggleHamburger(element) {
  $(element).parent().parent().find('.navbar-menu').toggleClass('is-active');
  $(element).toggleClass('is-active');
}
