$(document).ready(function() {
    // when user clicks add more btn of images
  $('.add-columns').click(function(ev) {
      ev.preventDefault();
      var count = $('#item-columns').children().length;
      var tmplMarkup = $('#columns-template').html();
      var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
      $('#item-columns').append(compiledTmpl);

      // update form count
      $('#id_columns-TOTAL_FORMS').attr('value', count+1);
  });
});
