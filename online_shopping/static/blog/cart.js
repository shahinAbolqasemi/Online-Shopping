$(function () {
    $("#delete_product").on("click", function (event) {
        event.preventDefault();
        let id = $(this).attr("id");
        let tr = $(this).closest("tr");
        let price = parseFloat(tr.find(".price").html());
        let numbers = parseFloat(tr.find(".numbers").html());
        const url = 'http://127.0.0.1:5000/delete_order_product/';
        $.ajax({
            url: url,
            data: JSON.stringify({id: id}),
            method: "POST",
            headers: {
                // "X-CSRFToken": csrftoken
            },
            crossDomain: true,
        })
            .done(function (result) {
                let $total = $("#products_sum")
                let total_price = parseFloat($total.html());
                $total.html(toString(total_price - price * numbers));
                $("#orderCount").html(result['badge_number']);
                tr.remove();
                alert("درخواست با موفقیت حذف شد")
            })
            .fail(function (error) {
                alert("درخواست شما انجام نشد" + error);
            });
    });
});