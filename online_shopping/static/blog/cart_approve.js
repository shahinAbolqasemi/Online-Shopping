$(function () {
    $("#finalizing").on("click",function (event) {
        event.preventDefault();
        let data = JSON.stringify({
            "first_name": $("#first_name").val(),
            "last_name": $("#last_name").val(),
            "date": $("#date").val(),
            "address": $("#address").val(),
            "telephone": $("#phoneNumber").val()
        });

        $.ajax({
            url: 'http://127.0.0.1:5000/order_final/',
            data: data,
            method: "POST",
            headers: {
                // "X-CSRFToken": csrftoken
            },
            crossDomain: true,
        })
            .done(function (result) {
                $("#orderCount").html(result['badge_number']);
                alert("ثبت نهایی سفارش با موفقیت انجام شد")
                document.location = 'http://127.0.0.1:5000/';
            })
            .fail(function (error) {
                alert("درخواست شما ثبت نشد" + error);
            });
    });
});