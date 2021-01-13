var $modal = $("#order-check-modal");
var $orderCheckButtons = $("button.order-check")
$orderCheckButtons.click(function (e) {
    e.preventDefault();
    var $this = $(this)
    var $orderCheckBtnText = $this.find(".order-check-text")
    console.log($orderCheckBtnText)
    var $orderCheckBtnSpinner = $this.find(".spinner-border")
    $orderCheckBtnText.addClass("visually-hidden")
    $orderCheckBtnSpinner.removeClass("visually-hidden")
    $orderCheckButtons.prop('disabled', true)
    var orderId = $this.attr('data-order-id')
    var url = `http://127.0.0.1:5000/api/order/${orderId}/`;
    $.get(url, function (resp) {
        var $newModal = $modal.clone();
        var $prodDetailTbody = $newModal.find("table tbody")
        var $prodDetailTr = $prodDetailTbody.find("tr").remove()
        var modal = new bootstrap.Modal($newModal[0]);
        var id = 1
        var data = resp.data
        var cusFullname = data.customerFirstName + ' ' + data.customerLastName
        var cusAddress = data.address
        var cusPhone = data.customerCellPhoneNum
        var deliveryDate = data.deliveryDate
        var orderDate = data.date
        var purchasedProductsId = data.purchasedProductsId
        $newModal.find(".customer-fullname").html(cusFullname);
        $newModal.find(".customer-address").html(cusAddress);
        $newModal.find(".customer-cellphone-number").html(cusPhone);
        $newModal.find(".customer-delivery-date").html(deliveryDate);
        $newModal.find(".customer-order-date").html(orderDate);
        purchasedProductsId.forEach(function(product){
            var $newProdTr = $prodDetailTr.clone()
            $newProdTr.find(".pro-id").html(id++);
            $newProdTr.find(".pro-name").html(product.name);
            $newProdTr.find(".pro-price").html(product.price);
            $newProdTr.find(".pro-warehouse").html(product.warehouseName);
            $newProdTr.find(".pro-quantity").html(product.count);
            $prodDetailTbody.append($newProdTr)
        })
        modal.show();
        $orderCheckBtnText.removeClass("visually-hidden")
        $orderCheckBtnSpinner.addClass("visually-hidden")
        $orderCheckButtons.prop('disabled', false)
    });
});
