//SWIPPER EVENT HANDLER CODE
 // Init after DOM loaded
document.addEventListener('DOMContentLoaded', function () {
   const swiper = new Swiper('.myProductCarousel', {
      loop: false,
      spaceBetween: 16,
      // Helpful when content/layout may change
      observer: true,
      observeParents: true,
      watchOverflow: true,
      pagination: { el: '.swiper-pagination', clickable: true },
      navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
      breakpoints: {
         0:   { slidesPerView: 1 },   // Mobile
         678: { slidesPerView: 2 },
         992: { slidesPerView: 3 },   // Tablet
         1124: { slidesPerView: 4 }    // Desktop / large
      },
      on: {
         init() { console.log('Swiper initialized — slides:', this.slides.length); }
      }
   });

   // Expose for debugging in console
   window.__mySwiper = swiper;
});



document.addEventListener('DOMContentLoaded', function () {
   const swiper = new Swiper('.commentCarousel', {
      loop: false,
      spaceBetween: 16,
      // Helpful when content/layout may change
      observer: true,
      observeParents: true,
      watchOverflow: true,
      pagination: { el: '.swiper-pagination', clickable: true },
      navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
      breakpoints: {
         0:   { slidesPerView: 1 },   // Mobile
         768: { slidesPerView: 2 },   // Tablet
         992: { slidesPerView: 2 }    // Desktop / large
      },
      on: {
         init() { console.log('Swiper initialized — slides:', this.slides.length); }
      }
   });

   // Expose for debugging in console
   window.__mySwiper = swiper;
});



document.addEventListener('DOMContentLoaded', function () {
   const swiper = new Swiper('.galleryCarousel', {
      loop: false,
      spaceBetween: 16,
      // Helpful when content/layout may change
      observer: true,
      observeParents: true,
      watchOverflow: true,
      pagination: { el: '.swiper-pagination', clickable: true },
      navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
      breakpoints: {
         0:   { slidesPerView: 2 },   // Mobile
         768: { slidesPerView: 3 },   // Tablet
         992: { slidesPerView: 4 }    // Desktop / large
      },
      on: {
         init() { console.log('Swiper initialized — slides:', this.slides.length); }
      }
   });

   // Expose for debugging in console
   window.__mySwiper = swiper;
});