// delete product
$("#deleteProduct").click(function (e) {
  e.preventDefault();
  var $tr = $(this).closest("tr");
  var $productId = $tr.attr("data-product-id");
  // console.log("product id", $productId);
  var url = `http://127.0.0.1:5000/api/product/delete/${$productId}/`;
  $("#deleteModal #saveBtnDelete").click(function (e) {
    // console.log(url)
    $.ajax({
      url: url,
      data: { productId: $productId },
      method: "GET",
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
  });
});

// edit product
$("#editProduct").click(function (e) {
  e.preventDefault();
  var $tbody = $("tbody");
  var $tr = $(this).closest("tr");
  var $productId = $(this).attr("data-product-id");
  var url = "http://127.0.0.1:5000/api/product/edit/";

  $("#editModal #saveBtnEdit").click(function () {
    var $name = $("#productName").val();
    var $image = "img src='" + $("#productImage").val() + "'>";
    var $category = $("#productCategory").val();
    var $description = $("#productDescription").val();
    var row = "<tr data-product-id='" + $productId + "'>";
    row += "<td>" + $image + "</td>";
    row += "<td>" + $name + "</td>";
    row += "<td>" + $category + "</td>";
    row += "</tr>";
    $.ajax({
      url: url,
      data: {
        productId: $productId,
        image: $("#productImage"),
        name: $name,
        category: $category,
        description: $description,
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
  });
});

// add product
$("#addProduct").click(function (e) {
  e.preventDefault();
  var $tbody = $("tbody");
  var url = "http://127.0.0.1:5000/api/product/add/";

  $("#addModal #saveBtnAdd").click(function () {
    var $name = $("#productName").val();
    var $image = "img src='" + $("#productImage").val() + "'>";
    var $category = $("#productCategory").val();
    var $description = $("#productDescription").val();
    var row = "<tr>";
    row += "<td>" + $image + "</td>";
    row += "<td>" + $name + "</td>";
    row += "<td>" + $category + "</td>";
    row += "</tr>";
    $.ajax({
      url: url,
      data: {
        image: $("#productImage"),
        name: $name,
        category: $category,
        description: $description,
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
          row.slice(0, 3) + " data-product-id='" + result.product_id + "'";
        row = row.replace("<tr", tag);
        $($tbody).prepend(row);
      })
      .fail(function (error) {
        alert("error");
      });
  });
});
