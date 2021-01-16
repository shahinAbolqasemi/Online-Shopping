// Add quantity
$(".addQuantity").click(function (e) {
  e.preventDefault();
  var $tbody = $("tbody");
  var url = "http://127.0.0.1:5000/api/quantity/add/";

  $("#addModal .saveBtnAdd").click(function () {
    var $productName = $("#productName").val();
    var $warehouseName = $("#warehouseName").val();
    var $price = $("#price").val();
    var $quantity = $("#quantity").val();
    var row = "<tr>";
    row += "<td>" + $warehouseName + "</td>";
    row += "<td>" + $productName + "</td>";
    row += "<td>" + $price + "</td>";
    row += "<td>" + $quantity + "</td>";
    row += "<td><button type='button' class='btn btn-link editQuantity' data-bs-toggle='modal' data-bs-target='#editModal'>ویرایش </button>";
    row += "<button type='button' class='btn btn-link deleteQuantity' data-bs-toggle='modal' data-bs-target='#deleteModal'>حذف </button></td>";
    row += "</tr>";
    $.ajax({
      url: url,
      data: {
        warehouseName: $warehouseName,
        productName: $productName,
        price: $price,
        quantity: $quantity,
      },
      method: "POST",
      headers: {
        // "X-CSRFToken": csrftoken
      },
      crossDomain: true,
    })
      .done(function (result) {
        // $($tr).remove();
        var tag =
          row.slice(0, 3) + " data-warehouse-id='" + result.data.warehouse_id + "' data-product-id='" + result.data.product_id +"'";
        row = row.replace("<tr", tag);
        $($tbody).prepend(row);
      })
      .fail(function (error) {
        alert("error");
      });
      $("#addModal").modal("toggle");
  });
});

// Edit Quantity
$(".editQuantity").click(function (e) {
  e.preventDefault();
  var $tbody = $("tbody");
  var $tr = $(this).closest("tr");
  var $warehouseId = $tr.attr("data-warehouse-id");
  var $productId = $tr.attr("data-product-id");
  var url = "http://127.0.0.1:5000/api/quantity/edit/";

  $("#editModal .saveBtnEdit").click(function () {
    var $productName = $("#productName").val();
    var $warehouseName = $("#warehouseName").val();
    var $price = $("#price").val();
    var $quantity = $("#quantity").val();
    var row =
      "<tr data-warehouse-id='" +
      $warehouseId +
      "' data-product-id='" +
      $productId +
      "'>";
    row += "<td>" + $warehouseName + "</td>";
    row += "<td>" + $productName + "</td>";
    row += "<td>" + $price + "</td>";
    row += "<td>" + $quantity + "</td>";
    row += "<td><button type='button' class='btn btn-link editQuantity' data-bs-toggle='modal' data-bs-target='#editModal'>ویرایش </button>";
    row += "<button type='button' class='btn btn-link deleteQuantity' data-bs-toggle='modal' data-bs-target='#deleteModal'>حذف </button></td>";
    row += "</tr>";
    $.ajax({
      url: url,
      data: {
        warehouseName: $warehouseName,
        productName: $productName,
        price: $price,
        quantity: $quantity,
      },
      method: "POST",
      headers: {
        // "X-CSRFToken": csrftoken
      },
      crossDomain: true,
    })
      .done(function (result) {
        $($tr).remove();
        $($tbody).prepend(row);
      })
      .fail(function (error) {
        alert("error");
      });
      $("#editModal").modal("toggle");
  });
});

// Delete Quantity
$(".deleteQuantity").click(function (e) {
  e.preventDefault();
  var $tr = $(this).closest("tr");
  var $warehouseId = $tr.attr("data-warehouse-id");
  var $productId = $tr.attr("data-product-id");
  // console.log("product id", $productId);
  var url = "http://127.0.0.1:5000//quantity/delete/";
  $("#deleteModal .saveBtnDelete").click(function (e) {
    // console.log(url)
    $.ajax({
      url: url,
      data: { productId: $productId, warehouseId: $warehouseId },
      method: "POST",
      headers: {
        // "X-CSRFToken": csrftoken
      },
      crossDomain: true,
    })
      .done(function (result) {
        $($tr).remove();
      })
      .fail(function (error) {
        alert("error");
      });
      $("#deleteModal").modal("toggle");
  });
});
