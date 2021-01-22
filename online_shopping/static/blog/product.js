$(function () {
    $("#add_to_cart").on("click", function (event) {
        event.preventDefault();
        let number = $("#number").val();
        let id = $("#add_to_cart").attr("data-order-id");
        let data = {numbers: number, id: id};
        const url = 'http://127.0.0.1:5000/order/add/';
        $.ajax({
            url: url,
            data: data,
            method: "POST",
            })
            .done(function (result) {
                $("#buyCount").html(result["result"]);
                alert("درخواست با موفقیت انجام شد");
            })
            .fail(function () {
                alert("درخواست شما ثبت نشد");
            });
    });
});