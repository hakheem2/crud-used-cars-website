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

	// opening and closing report section
	$('#open-report').on('click', function() {
		$('#full-report').addClass('open');
	});

	$('.btn-close').on('click', function() {
		$('#full-report').removeClass('open');
	});

	// function for opening and closing of order form
	$('.buy').on('click', function(e) {
		e.stopPropagation();
		$('#order-form').addClass('open');
	});

	$(document).on("click", function () {
		$('#order-form').removeClass('open');
	});

	$('#order-form *').on('click', function(e){
		e.stopPropagation();
	});

	// random numbers for views section
	// Generate random number between 1 and 15
	var randomNum = Math.floor(Math.random() * 15) + 1;
	$('.view-no').text(randomNum);

	// Generate calendar: only future dates starting tomorrow
	// Dates
	let today = new Date();
	let tomorrow = new Date(today);
	tomorrow.setDate(today.getDate() + 1);

	let calendarDiv = $("#calendar");
	let month = tomorrow.getMonth();
	let year = tomorrow.getFullYear();

	function renderCalendar(month, year) {
		calendarDiv.empty();
		let daysInMonth = new Date(year, month + 1, 0).getDate();
		let firstDay = new Date(year, month, 1).getDay();

		// Add blank slots for alignment
		for (let i = 0; i < firstDay; i++) {
			calendarDiv.append("<div></div>");
		}

		for (let d = 1; d <= daysInMonth; d++) {
			let date = new Date(year, month, d);
			let btn = $("<button type='button'>")
				.text(d)
				.attr("data-date", date.toISOString().split('T')[0]);

			// Mark today
			if (date.toDateString() === today.toDateString()) {
				btn.addClass("today");
			}

			// Disable past & today (only allow tomorrow onwards)
			if (date < tomorrow) {
				btn.prop("disabled", true);
			}

			// Pre-select tomorrow’s date
			if (date.toDateString() === tomorrow.toDateString()) {
				btn.addClass("selected");
				$("#selected-date").val(date.toISOString().split("T")[0]);
			}

			btn.on("click", function(){
				$("#calendar button").removeClass("selected");
				$(this).addClass("selected");
				$("#selected-date").val($(this).data("date"));
			});

			calendarDiv.append(btn);
		}
	}

	renderCalendar(month, year);

	// Time slots (10am–9pm)
	let times = [];
	for (let h = 10; h <= 21; h++) {
		let ampm = h < 12 ? "am" : "pm";
		let hour = h % 12 === 0 ? 12 : h % 12;
		times.push(hour + ":00 " + ampm);
	}

	times.forEach(t => {
		let btn = $("<button type='button'>")
			.text(t)
			.attr("data-time", t);

		// ✅ Pre-select 10:00 am
		if (t === "10:00 am") {
			btn.addClass("selected");
			$("#selected-time").val(t);
		}

		btn.on("click", function(){
			$("#timeSlots button").removeClass("selected");
			$(this).addClass("selected");
			$("#selected-time").val($(this).data("time"));
		});

		$("#timeSlots").append(btn);
	});

	let postUrl = $("#testDriveForm").data("url");
	$("#testDriveForm").on("submit", function (e) {
		e.preventDefault();
		$.ajax({
			url: postUrl,  // Django view URL
			type: "POST",
			data: {
				name: $("#name").val(),
				phone: $("#phone").val(),
				email: $("#email").val(),
				date: $("#selected-date").val(),
				time: $("#selected-time").val(),
				car_id: $("#car-id").val()
			},
			headers: { "X-CSRFToken": csrftoken },
			success: function (response) {
				$("#FormErrors").empty();
				if (response.status === "success") {
					$("#testDriveModal").modal("hide");

					// Format selected date
					let rawDate = $("#selected-date").val(); // e.g. "2025-09-06"
					let dateObj = new Date(rawDate);
					let options = { weekday: 'long', day: 'numeric', month: 'long' };
					let formattedDate = dateObj.toLocaleDateString('en-US', options);
					// -> "Saturday, September 6"
					// If you prefer "Saturday 6 September", we can rearrange:

					formattedDate = formattedDate.replace(",", ""); // remove comma

					// Update scheduled info
					$("#scheduled-date").text(formattedDate);
					$("#scheduled-time").text($("#selected-time").val());

					// Open success modal
					$("#successModal").modal("show");
				}else {
                // If somehow we got an error in success callback
                $("#FormErrors").html("<p>" + response.message + "</p>");
            }
			},
			error: function (xhr) {
            // Clear old errors
            $("#FormErrors").empty();

            let msg = "Something went wrong. Please try again.";
            if (xhr.responseJSON && xhr.responseJSON.message) {
                msg = xhr.responseJSON.message;
            }
            $("#FormErrors").html("<p>" + msg + "</p>");
        },
		});
	});

});
