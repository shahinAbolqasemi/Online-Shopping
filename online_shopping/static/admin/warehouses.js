// Add warehouse
$("#addWarehouse").click(function (e) {
  e.preventDefault();
  var $tbody = $("tbody");
  var url = "http://127.0.0.1:5000/api/warehouse/add/";
  $("#addModal #saveBtnAdd").click(function () {
    var $name = $("#warehouseName").val();
    var row = "<tr>";
    row += "<td>" + $name + "</td>";
    row += "</tr>";
    $.ajax({
      url: url,
      data: { name: $name },
      method: "POST",
      headers: {
        // "X-CSRFToken": csrftoken
      },
      crossDomain: true,
    })
      .done(function (result) {
        var tag =
          row.slice(0, 3) + " data-warehouse-id='" + result.warehouse_id + "'";
        row = row.replace("<tr", tag);
        $($tbody).prepend(row);
      })
      .fail(function (error) {
        alert("error");
      });
  });
});

// Edit warehouse
$("#editWarehouse").click(function (e) {
  e.preventDefault();
  var $tbody = $("tbody");
  var $tr = $(this).closest("tr");
  var $warehouseId = $tr.attr("data-warehouse-id");
  var url = "http://127.0.0.1:5000/api/warehouse/edit/";
  $("#editModal #saveBtnEdit").click(function () {
    var $name = $("#warehouseName").val();
    var row = "<tr data-warehouse-id='" + $warehouseId + "'>";
    row += "<td>" + $name + "</td>";
    row += "</tr>";
    $.ajax({
      url: url,
      data: { warehouseId: $warehouseId, name: $name },
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

// Delete warehouse
$("#deleteWarehouse").click(function (e) {
  e.preventDefault();
  var $tr = $(this).closest("tr");
  var $warehouseId = $tr.attr("data-product-id");
  console.log($warehouseId);
  var url = `http://127.0.0.1:5000/api/warehouse/delete/${$warehouseId}/`;
  $("#deleteModal #saveBtnDelete").click(function (e) {
    // console.log(url)
    $.ajax({
      url: url,
      data: { warehouseId: $warehouseId },
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
