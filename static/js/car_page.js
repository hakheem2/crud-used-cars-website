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



   //opening and closing report section
   $('#open-report').on('click', function() {
      $('#full-report').addClass('open');     
   })

   $('.btn-close').on('click', function() {
      $('#full-report').removeClass('open');
   })

   
   //function for opening and closing of rder form
   $('.buy').on('click', function(e) {
      e.stopPropagation();
      $('#order-form').addClass('open');     
   })

   $(document).on("click", function () {
      $('#order-form').removeClass('open'); 
    });
   
   $('#order-form *').on('click', function(e){
      e.stopPropagation();
   });


   //randmon numbers for views section
   // Generate random number between 1 and 15
    var randomNum = Math.floor(Math.random() * 15) + 1;
    $('.view-no').text(randomNum);

});
   
   
  