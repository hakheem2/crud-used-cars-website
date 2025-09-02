$(document).ready(function(){
   // ---------- nav bar open and close ---------
  $("#nav_open").click(function(){
    $("#sidebar").addClass('open');
  });

  $("#nav_close").click(function(){
    $("#sidebar").removeClass('open');
  });


  let currentPage = window.location.pathname; 

  $(".nav_menu .nav_link").each(function() {
      let linkPath = $(this).attr("href");
      
      // normalize paths (remove trailing slashes before comparing)
      if (linkPath.replace(/\/$/, "") === currentPage.replace(/\/$/, "")) {
          $(this).addClass("active");
      }
  });

  $(".side_menu .nav_link").each(function() {
    let linkPath = $(this).attr("href");
    
    // normalize paths (remove trailing slashes before comparing)
    if (linkPath.replace(/\/$/, "") === currentPage.replace(/\/$/, "")) {
        $(this).addClass("active");
    }
  });

  
});
