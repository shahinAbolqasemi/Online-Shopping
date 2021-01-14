$(function () {
    $("#finalizing").click(function (event) {
        event.preventDefault();
        let data = {
            "first_name": $("#first_name").val(),
            "last_name": $("#last_name").val(),
            "date": $("#date").val(),
            "address": $("#address").val(),
            "telephone": $("#phoneNumber").val()
        };
        const url = window.location.href + 'add_order';
        $.post(url, data, function (res) {
            if (res["status"] === "success") {
                window.location.replace('http://127.0.0.1:5000/');
                alert("ثبت نهایی سفارش با موفقیت انجام شد")
            } else {
                alert("درخواست با خطا مواجه شد")
            }
        });
    });
});