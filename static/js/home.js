$(document).ready(function() {
  const $car = $("#car");
  const $wheelFront = $(".wheel_front");
  const $wheelBack = $(".wheel_back");

  function isInViewport($elem) {
    const elementTop = $elem.offset().top;
    const elementBottom = elementTop + $elem.outerHeight();
    const viewportTop = $(window).scrollTop();
    const viewportBottom = viewportTop + $(window).height();
    return elementBottom > viewportTop && elementTop < viewportBottom;
  }

  function triggerCarAnimation() {
    if (isInViewport($car) && !$car.hasClass("slide-in")) {
      $car.addClass("slide-in");          // slide in car
      $wheelFront.addClass("rotate");     // rotate front wheel
      $wheelBack.addClass("rotate");      // rotate back wheel
    }
  }


  // Check on scroll/resize
  $(window).on("scroll resize", triggerCarAnimation);



  //setting backgound video at find car section
  var $video = $("#car_vid");

   function setVideo() {
      if ($(window).width() <= 1024) {
         // Mobile / tablet
         $video.attr("poster", $video.data("poster-sm"));
         $video.html(`<source src="${$video.data("src-sm")}" type="video/mp4">`);
      } else {
         // Desktop
         $video.attr("poster", $video.data("poster-lg"));
         $video.html(`<source src="${$video.data("src-lg")}" type="video/mp4">`);
      }

      // Reload and play
      $video[0].load();
      $video[0].play();
   }

   // Run once on page load
   setVideo();

   // Optional: update on resize
   $(window).on("resize", function () {
      setVideo();
   });



   // toogling comment text
   $('.toogle_comment').on('click', function() {
      var $text = $(this).closest('.comment-card').find('.text');
      $text.toggleClass('expanded');
      $(this).text($text.hasClass('expanded') ? 'Read Less' : 'Read More');
   });



   $(".faq_card .head").on("click", function () {
      let $faqCard = $(this).parent();
      let $body = $faqCard.find(".body");
      let $icon = $(this).find("svg");

      // Close all other bodies
      $(".faq_card .body").not($body).slideUp(300).removeClass("expanded");
      $(".faq_card .head svg").not($icon).removeClass("rotated");

      // Toggle the clicked one
      if ($body.hasClass("expanded")) {
         $body.slideUp(300).removeClass("expanded");
         $icon.removeClass("rotated");
      } else {
         $body.slideDown(300).addClass("expanded");
         $icon.addClass("rotated");
      }
   });
   
});
