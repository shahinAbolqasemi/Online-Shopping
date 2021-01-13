$(function () {
    $("#add-to-cart").click(function () {
        let $number = $("#number").val()
        let $id = $("#add-to-cart").getAttribute("data-order-id")
        let $data = {numbers:$number, id:$id}
        const url = window.location.href + 'add_order';
        $.post(url, $data, function (data, status) {
            $("#orderCount").html(data);
            if (status === "success"){
                alert("درخواست با موفقیت انجام شد")
            } else {
                alert("درخواست شما ثبت نشد")
            }
        })


    })

})