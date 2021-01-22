// Add warehouse
$(".addWarehouse").click(function (e) {
  e.preventDefault();
  var $tbody = $("tbody");
  var url = "http://127.0.0.1:5000/api/warehouse/add/";
  $("#addModal .saveBtnAdd").click(function () {
    var $name = $("#warehouseName").val();
    var row = "<tr>";
    row += "<td>" + $name + "</td>";
    row += "<td><button type='button' class='btn btn-link editWarehouse' data-bs-toggle='modal' data-bs-target='#editModal'>ویرایش </button>";
    row += "<button type='button' class='btn btn-link deleteWarehouse' data-bs-toggle='modal' data-bs-target='#deleteModal'>حذف </button></td>";
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
          // console.log(result);
        var tag =
          row.slice(0, 3) + " data-warehouse-id='" + result.data.warehouseId + "'";
        row = row.replace("<tr", tag);
        console.log("row: ", row);
        $($tbody).prepend(row);
        console.log('done');
      // $("#addModal").modal("toggle");
      })
      .fail(function (error) {
        alert("error");
      // $("#addModal").modal("toggle");
      });
  $("#addModal").modal("toggle");
  });
});

// Edit warehouse
$(".editWarehouse").click(function (e) {
  e.preventDefault();
  var $tbody = $("tbody");
  var $tr = $(this).closest("tr");
  var $warehouseId = $tr.attr("data-warehouse-id");
  var url = "http://127.0.0.1:5000/api/warehouse/edit/";
  $("#editModal .saveBtnEdit").click(function () {
    var $name = $("#warehouseName").val();
    var row = "<tr data-warehouse-id='" + $warehouseId + "'>";
    row += "<td>" + $name + "</td>";
    row += "<td><button type='button' class='btn btn-link editWarehouse' data-bs-toggle='modal' data-bs-target='#editModal'>ویرایش </button>";
    row += "<button type='button' class='btn btn-link deleteWarehouse' data-bs-toggle='modal' data-bs-target='#deleteModal'>حذف </button></td>";
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
        // console.log('done');
        // $("#editModal").modal("toggle");
      })
      .fail(function (error) {
        alert("error");
      // $("#editModal").modal("toggle");
      });
      $("#editModal").modal("toggle");
  });
});

// Delete warehouse
$(".deleteWarehouse").click(function (e) {
  e.preventDefault();
  var $tr = $(this).closest("tr");
  // console.log("this: ", $(this));
  // console.log("tr: ", $tr);
  var $warehouseId = $tr.attr("data-warehouse-id");
  // console.log($warehouseId);
  var url = `http://127.0.0.1:5000/api/warehouse/delete/${$warehouseId}/`;
  $("#deleteModal .saveBtnDelete").click(function (e) {
    // console.log(url)
    $.ajax({
      url: url,
      // data: { warehouseId: $warehouseId },
      method: "GET",
      headers: {
        // "X-CSRFToken": csrftoken
      },
      crossDomain: true,
    })
      .done(function (result) {
        $tr.remove();
        // console.log('done');
      })
      .fail(function (error) {
        alert("error");
      });
  $("#deleteModal").modal("toggle");
  });
});
