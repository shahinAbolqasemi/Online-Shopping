$(function () {
    $("#delete_product").click(function (event) {
        event.preventDefault();
        let delete_btn = $("#delete_product");
        let id = delete_btn.attr("id");
        let tr = delete_btn.closest("tr");
        let price = parseFloat(tr.find(".price").html());
        let numbers = parseFloat(tr.find(".numbers").html());
        const url = window.location.href + 'delete_order_product';
        $.post(url, JSON.stringify({id: id}), function (res) {
            if (res['status'] === "success") {
                let $total = $("#products_sum")
                let total_price = parseFloat($total.html());
                $total.html(total_price - price * numbers);
                $("#orderCount").html(res['badge_number']);
                tr.remove();
                alert("درخواست با موفقیت حذف شد")
            } else {
                alert("درخواست شما انجام نشد")
            }
        });
    });
});