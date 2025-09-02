$(document).ready(function() {
   const wishlistUrl = $('#ajax-wishlist-url').val();
   
   // Fetch wishlist from session on page load
   $.get(wishlistUrl, function(data) {
      if (data.success && data.wishlist) {
         updateWishlistUI(data.wishlist);
      }
   });

   // Toggle wishlist on click
   $(document).on('click', '.wishlist-btn', function(e) {
      e.preventDefault();
      const carId = $(this).data('id');
      const $btn = $(this);

      $.get(wishlistUrl, {car_id: carId}, function(data) {
         if (data.success) {
               if (data.in_wishlist) {
                  $btn.addClass('in-wishlist');
                  $btn.find('svg').attr('fill', '#FE3447').attr('stroke', '#FE3447');
               } else {
                  $btn.removeClass('in-wishlist');
                  $btn.find('svg').attr('fill', 'none').attr('stroke', '#082c33');
               }
         }
      });
   });
});


const wishlistUrl = $('#ajax-wishlist-url').val();

// Function to update hearts for all wishlist buttons
function updateWishlistUI(wishlist) {
$('.wishlist-btn').each(function() {
   const carId = $(this).data('id').toString();
   if (wishlist.includes(carId)) {
         $(this).addClass('in-wishlist');
         $(this).find('svg').attr('fill', '#FE3447').attr('stroke', '#FE3447');
   } else {
         $(this).removeClass('in-wishlist');
         $(this).find('svg').attr('fill', 'none').attr('stroke', '#082c33');
   }
});
}
