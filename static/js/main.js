$(function () {

  var $goToTop = $('#vaccine-footer a.go-to-top');
  var $navBar = $('nav#vaccine-main-nav');

  // Back to button script.
  var backToTop = function () {
    $goToTop.on('click', function (event) {
      event.preventDefault();
      $('html, body').animate({
        scrollTop: 0
      }, 1000);
    })
  };

  // Toggle main navigation script.
  var toggleFixedNavBar = function () {
    $navBar.toggleClass('fixed', $(window).scrollTop() > 100);
  };

  // Date picker script for date field.
  var datePicker = function () {
    var $dateField = $('input[id="date"]');
    var $container = $('#signup-form');

    $dateField.datepicker({
      format: 'dd/mm/yyyy',
      startDate: '01/01/2017',
      container: $container,
      todayHighlight: true,
      autoclose: true,
      orientation: 'bottom'
    });
  };

  // Toggle main navigation on scroll.
  $(window).on('scroll', function () {
    toggleFixedNavBar();
  });

  backToTop();
  toggleFixedNavBar();
  datePicker();
});
