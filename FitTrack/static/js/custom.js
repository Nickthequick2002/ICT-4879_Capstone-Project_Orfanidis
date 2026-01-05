/** This script is from the AOS animation library
 * and was not created by me
 */

$(function () {

  // MENU
  $('.navbar-collapse a').on('click', function () {
    $('.navbar-collapse').collapse('hide');
  });

  // AOS ANIMATION
  AOS.init({
    disable: 'mobile',
    duration: 800,
    anchorPlacement: 'center-bottom'
  });

  // SMOOTHSCROLL NAVBAR
  $(function () {
    $('.navbar a[href^="#"], .hero-text a[href^="#"]').on('click', function (event) {
      var $anchor = $(this);
      $('html, body').stop().animate({
        scrollTop: $($anchor.attr('href')).offset().top - 49
      }, 1000);
      event.preventDefault();
    });
  });
});
