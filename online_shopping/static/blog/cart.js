$(function () {
    $("#delete_product").click(function (event) {
        event.preventDefault();
        let $delete = $("#delete_product");
        let $id = $delete.attr("id");
        let $tr = $delete.closest("tr");
        let $price = parseFloat($tr.find(".price").html());
        let $numbers = parseFloat($tr.find(".numbers").html());
        const url = window.location.href + 'add_order';
        $.post(url, JSON.stringify({ id: $id }), function (res) {
            if (res['status'] === "success"){
                let $total_price = parseFloat($("#products_sum").html());
                $total_price.html($total_price - $price * $numbers);
                $("#orderCount").html(res['badge_number']);
                $tr.remove();
                alert("درخواست با موفقیت حذف شد")
            } else {
                alert("درخواست شما انجام نشد")
            }
        });
    });
});