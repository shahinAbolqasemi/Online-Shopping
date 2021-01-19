$(function () {
    $("#add_to_cart").on("click", function (event) {
        event.preventDefault();
        let number = $("#number").val();
        let id = $("#add_to_cart").attr("data-order-id");
        let data = JSON.stringify({numbers: number, id: id});
        $.ajax({
            url: 'http://127.0.0.1:5000/add_order/',
            data: data,
            method: "POST",
            headers: {
                // "X-CSRFToken": csrftoken
            },
            crossDomain: true,
        })
            .done(function (result) {
                $("#orderCount").html(result['badge_number']);
                alert("درخواست با موفقیت انجام شد");
            })
            .fail(function (error) {
                alert("درخواست شما ثبت نشد" + error);
            });
    });
});