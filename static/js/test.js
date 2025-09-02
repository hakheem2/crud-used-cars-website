$(document).ready(function () {
    //  OPENING AND CLOSING FILTER SIDEBAR
    $('#openFilters').on("click", function () {
        $('#filters').addClass('open');
    });
    $('#closeFilters').on("click", function () {
        $('#filters').removeClass('open');
    });



    // === 1. OPEN / CLOSE FILTER DROPDOWN ===
    $(".filter-dropdown .drop-input").on("click", function (e) {
        if ($(e.target).closest(".tag, .remove-tag").length) {
            return;
        }
        e.stopPropagation(); // prevent bubbling
        let $dropdown = $(this).closest(".filter-dropdown");
        $(".filter-dropdown").not($dropdown).removeClass("open"); // close others
        $dropdown.toggleClass("open"); // toggle current
    });

    // Close dropdown when clicking outside
    $(document).on("click", function () {
        $(".filter-dropdown").removeClass("open");
    });

    // === 2. SELECT ITEM FROM DROPDOWN ===
    $(".filter-dropdown .dropdown-item").on("click", function (e) {
        e.stopPropagation();

        let $dropdown = $(this).closest(".filter-dropdown");
        let value = $(this).data("value");
        let text = $(this).text();

        // prevent duplicate selection
        if ($dropdown.find(".selected-tags span[data-value='" + value + "']").length === 0) {
            let tag = `
                <span class="tag" data-value="${value}">
                    ${text} <span class="remove-tag">&times;</span>
                </span>
            `;
            $dropdown.find(".selected-tags").append(tag);
        }
    });

    // === 3. REMOVE INDIVIDUAL TAG ===
    $(document).on("click", ".tag", function (e) {
        e.stopPropagation();
        $(this).remove();
    });

    // RESETING ALL FLTERS
    function resetAllFilters() {
    // Remove all selected tags
        $(".filter-dropdown .selected-tags").empty();

        // Re-enable all dropdown items (in case you were disabling them)
        $(".filter-dropdown .dropdown-item").removeClass("disabled");

        // Close dropdowns
        $(".filter-dropdown").removeClass("open");
    }

    $(".reset-filters").on("click", function () {
        resetAllFilters();
    });


    // product sorting project
     // ------------------------
    $(".sort-dropdown .drop-input").on("click", function (e) {
        e.stopPropagation();
        const root = $(this).closest(".sort-dropdown");
        root.find(".dropdown-list").toggleClass("open");
        root.find(".drop-icon").toggleClass("rotated");
    });

    $(document).on("click", function () {
        $(".sort-dropdown .dropdown-list").removeClass("open");
        $(".sort-dropdown .drop-icon").removeClass("rotated");
    });

    $(".sort-dropdown .dropdown-item").on("click", function (e) {
        e.stopPropagation();
        const sortKey = $(this).data("value");
        const label = $(this).text();
        $("#sort-value").text(label);
        $("#current-sort").val(sortKey);
        $(this).closest(".sort-dropdown").find(".dropdown-list").removeClass("open");
        $(this).closest(".sort-dropdown").find(".drop-icon").removeClass("rotated");
        $("#reset-sort").removeClass("d-none");
    });

    $("#reset-sort").on("click", function (e) {
        e.stopPropagation();
        $("#current-sort").val("all");
        $("#sort-value").text("Sort:");
        $(this).addClass("d-none");
    });



    function getSelectedFilters() {
        const filters = {};

        // Make
        filters.make = [];
        $("#filters .wrapper:has(h4:contains('Make')) .selected-tags .tag").each(function() {
            filters.make.push($(this).data('value'));
        });

        // Body Type
        filters.body_type = [];
        $("#filters .wrapper:has(h4:contains('Body Type')) .selected-tags .tag").each(function() {
            filters.body_type.push($(this).data('value'));
        });

        // Year
        filters.year = [];
        $("#filters .wrapper:has(h4:contains('Year')) .selected-tags .tag").each(function() {
            filters.year.push($(this).data('value'));
        });

        // Max Price
        const priceTag = $("#filters .wrapper:has(h4:contains('Max Price')) .selected-tags .tag").first();
        filters.max_price = priceTag.length ? priceTag.data('value') : '';

        // Max Mileage
        const mileageTag = $("#filters .wrapper:has(h4:contains('Max Mileage')) .selected-tags .tag").first();
        filters.max_mileage = mileageTag.length ? mileageTag.data('value') : '';

        // Current Sort
        filters.sort = $("#current-sort").val();

        return filters;
    }

    function loadCars() {
        const filters = getSelectedFilters();

        $.ajax({
            url: $('#ajax-car-url').val(),
            type: 'GET',
            data: filters,
            success: function(response) {
                $("#product-grid").html(response);
            },
            error: function() {
                console.error('Failed to load cars.');
            }
        });
    }

    // Trigger AJAX on filter tag add/remove
    $(document).on('click', '.filter-dropdown .dropdown-item', function() {
        alert('working')
        setTimeout(loadCars, 100); // slight delay to allow tag to be added
    });

    $(document).on('click', '.tag', function() {
        setTimeout(loadCars, 100); // slight delay to allow tag to be removed
    });

    // Trigger AJAX on sort change
    $(document).on('click', '.sort-dropdown .dropdown-item', function() {
        alert('working');
        setTimeout(loadCars, 100);
    });

    // Reset all filters
    $(".reset-filters").on("click", function() {
        setTimeout(loadCars, 100);
    });


});