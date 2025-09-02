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
        if ($(e.target).closest(".tag, .remove-tag").length) return;
        e.stopPropagation();
        let $dropdown = $(this).closest(".filter-dropdown");
        $(".filter-dropdown").not($dropdown).removeClass("open");
        $dropdown.toggleClass("open");
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

        // Determine if this dropdown is single-selection
        const isSingleSelection = 
        $dropdown.closest(".wrapper").data("filter") === "max_price" ||
        $dropdown.closest(".wrapper").data("filter") === "max_mileage" ||
        $dropdown.closest(".wrapper").data("filter") === "monthly_installment";

        if (isSingleSelection) {
            // Remove existing tag if any
            $dropdown.find(".selected-tags .tag").remove();
        } else {
            // prevent duplicate selection for multi-select filters
            if ($dropdown.find(".selected-tags span[data-value='" + value + "']").length > 0) return;
        }

        // Add the new tag
        let tag = `<span class="tag" data-value="${value}">${text} <span class="remove-tag">&times;</span></span>`;
        $dropdown.find(".selected-tags").append(tag);

        // Trigger AJAX load
        loadCars();
    });

    // === 3. REMOVE INDIVIDUAL TAG ===
    $(document).on("click", ".tag", function (e) {
        e.stopPropagation();
        $(this).remove();
        loadCars();
    });

    // RESETING ALL FLTERS
    function resetAllFilters() {
        $(".filter-dropdown .selected-tags").empty();
        $(".filter-dropdown .dropdown-item").removeClass("disabled");
        $(".filter-dropdown").removeClass("open");
    }

    $(".reset-filters").on("click", function () {
        resetAllFilters();
        loadCars();
    });

    // === 4. SORT DROPDOWN ===
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
        loadCars();
    });

    $("#reset-sort").on("click", function (e) {
        e.stopPropagation();
        $("#current-sort").val("all");
        $("#sort-value").text("Sort:");
        $(this).addClass("d-none");
        loadCars();
    });

    // === 5. GET SELECTED FILTERS ===
    function getSelectedFilters() {
        const filters = {};

        $("#filters .wrapper").each(function () {
            const filterName = $(this).data("filter");
            const tags = $(this).find(".selected-tags .tag").map(function () {
                return $(this).data("value");
            }).get();

            if (filterName === "max_price" || filterName === "max_mileage" || filterName === "monthly_installment") {
                filters[filterName] = tags.length ? tags[0] : '';
            } else {
                filters[filterName] = tags;
            }
        });

        // Include current sort
        filters.sort = $("#current-sort").val();

        return filters;
    }

    // === 6. AJAX LOAD CARS ===
    function loadCars() {
        const filters = getSelectedFilters();

        $.ajax({
            url: $('#ajax-car-url').val(),
            type: 'GET',
            data: filters,
            success: function (response) {
                $("#product-grid").html(response);

                const wishlistUrl = $('#ajax-wishlist-url').val();
                $.get(wishlistUrl, function(res) {
                    if (res.success && res.wishlist) {
                        updateWishlistUI(res.wishlist);
                    }
                });
            },
            error: function () {
                console.error('Failed to load cars.');
            }
        });
    }

    loadCars();
});
