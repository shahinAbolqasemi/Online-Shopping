$(function () {
    $("#add-to-cart").click(function (event) {
        event.preventDefault();
        let $number = $("#number").val();
        let $id = $("#add-to-cart").attr("data-order-id");
        let $data = JSON.stringify({numbers:$number, id:$id});
        const url = window.location.href + 'add_order';
        $.post(url, $data, function (data, status) {
            $("#orderCount").html(data['badge_number']);
            if (status === "success"){
                alert("درخواست با موفقیت انجام شد")
            } else {
                alert("درخواست شما ثبت نشد")
            }
        });
    });
});