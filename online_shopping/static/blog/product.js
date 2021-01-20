$(function () {
    $("#add_to_cart").on("click", function (event) {
        event.preventDefault();
        let number = $("#number").val();
        let id = $("#add_to_cart").attr("data-order-id");
        let data = JSON.stringify({numbers: number, id: id});
        const url = 'http://127.0.0.1:5000/api/order/add/';
        $.ajax({
            url: url,
            data: {numbers: number, id: id},
            method: "GET",
            success: function (data) {
                console.log("success");}

            })
            // .done(function (response) {
            //     // $("#orderCount").html(result);
            //     alert("درخواست با موفقیت انجام شد" + response);
            // })
            // .fail(function () {
            //     alert("درخواست شما ثبت نشد");
            // });
    });
});