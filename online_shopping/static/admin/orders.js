var $modal = $("#order-check-modal");
var modal = new bootstrap.Modal($modal[0]);
$("a.order-check").click(function (e) {
    e.preventDefault();
    modal.show();
});