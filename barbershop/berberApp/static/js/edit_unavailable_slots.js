document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#id_unavailable_dates", {
        dateFormat: "Y-m-d",
        minDate: "today",
        mode: "multiple"
    });
});
