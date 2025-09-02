$(document).ready(function() {
   
   // When a gallery image is clicked
   $('.gallery-img img').on('click', function() {
      var newSrc = $(this).attr('src'); // Get clicked image src
      var mainImage = $('.main-image img');

      // Fade out, change src, fade in
      mainImage.fadeOut(200, function() {
         mainImage.attr('src', newSrc).fadeIn(200);
      });
   });


   $('#open-report').on('click', function() {
      $('#full-report').addClass('open');     
   })

   $('.btn-close').on('click', function() {
      $('#full-report').removeClass('open');
   })

});
   
   
  