$(function () {
    $('#order_table button').on("click", function (event) {
        event.preventDefault();
        let id = $(this).attr("id");
        let tr = $(this).closest("tr");
        let price = parseFloat(tr.find(".price").html());
        let numbers = parseFloat(tr.find(".numbers").html());
        const url = 'http://127.0.0.1:5000/delete_order_product/';
        $.ajax({
            url: url,
            data: {id: id},
            method: "POST",
        })
            .done(function (result) {
                $("#buyCount").html(result["result"]);
                let $total = $("#products_sum")
                let total_price = parseFloat($total.html());
                $total.html(total_price - price * numbers);
                tr.remove();

                alert("درخواست با موفقیت حذف شد")
            })
            .fail(function () {
                alert("درخواست شما انجام نشد");
            });
    });
});