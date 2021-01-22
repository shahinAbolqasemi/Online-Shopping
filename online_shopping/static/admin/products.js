// delete product
$(".deleteProduct").click(function (e) {
  e.preventDefault();
  var $tr = $(this).closest("tr");
  var $productId = $tr.attr("data-product-id");
  // console.log("product id", $productId);
  var url = `http://127.0.0.1:5000/api/product/delete/${$productId}/`;
  $("#deleteModal .saveBtnDelete").click(function (e) {
    // console.log(url)
    $.ajax({
      url: url,
      // data: { productId: $productId },
      method: "GET",
      headers: {
        // "X-CSRFToken": csrftoken
      },
      crossDomain: true,
    })
      .done(function (result) {
        $($tr).remove();
        // console.log('done');
        //   $("#deleteModal").modal("toggle");
      })
      .fail(function (error) {
        alert("error");
      // $("#deleteModal").modal("toggle");
      });
      $("#deleteModal").modal("toggle");
  });
});

// edit product
$(".editProduct").click(function (e) {
  e.preventDefault();
  var $tbody = $("tbody");
  var $tr = $(this).closest("tr");
  var $productId = $(this).attr("data-product-id");
  var url = "http://127.0.0.1:5000/api/product/edit/";

  $("#editModal .saveBtnEdit").click(function () {
    var $name = $("#editModal .productName").val();
    var $category = $("#editModal .productCategory").val();
    var $description = $("#editModal .productDescription").val();
    var row = "<tr data-product-id='" + $productId + "'>";
    row += "<td>" + $name + "</td>";
    row += "<td>" + $category + "</td>";
    row += "<td><button type='button' class='btn btn-link editProduct' data-bs-toggle='modal' data-bs-target='#editModal'>ویرایش </button>";
    row += "<button type='button' class='btn btn-link deleteProduct' data-bs-toggle='modal' data-bs-target='#deleteModal'>حذف </button></td>";
    row += "</tr>";
    $.ajax({
      url: url,
      data: {
        productId: $productId,
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
      // $("#editModal").modal("toggle");
      })
      .fail(function (error) {
        alert("error");
      // $("#editModal").modal("toggle");
      });
      $("#editModal").modal("toggle");
  });
});

// add product
$(".addProduct").click(function (e) {
  e.preventDefault();
  var $tbody = $("tbody");
  var url = "http://127.0.0.1:5000/api/product/add/";

  $("#addModal .saveBtnAdd").click(function () {
    var $name = $("#addModal .productName").val();
    var $category = $("#addModal .productCategory").val();
    var $description = $("#addModal .productDescription").val();
    var fd = new FormData();
    var image = $("#addModal .productImage")[0].files;
    console.log('image:', image);
    console.log('image0: ', image[0]);
    // console.log($name);
    // console.log($category);
    // console.log(image);
    if (image.length > 0) {
      fd.append('image', image[0]);
    };
    fd.append('name', $name);
    fd.append('category', $category);
    fd.append('description', $description);
    console.log('fd', fd);
    console.log('image', fd.getAll('image'));
    var row = "<tr>";
    row += "<td>" + $name + "</td>";
    row += "<td>" + $category + "</td>";
    row += "<td><button type='button' class='btn btn-link editProduct' data-bs-toggle='modal' data-bs-target='#editModal'>ویرایش </button>";
    row += "<button type='button' class='btn btn-link deleteProduct' data-bs-toggle='modal' data-bs-target='#deleteModal'>حذف </button></td>";
    row += "</tr>";
    $.ajax({
      url: url,
      // data: {
      //   image: fd,
      //   name: $name,
      //   category: $category,
      //   description: $description,
      // },
      data: fd,
      method: "POST",
      processData: false,
      contentType: false,
      headers: {
        // "X-CSRFToken": csrftoken
      },
      crossDomain: true,
    })
      .done(function (result) {
        // $($tr).remove();
        var tag =
          row.slice(0, 3) + " data-product-id='" + result.data.productId + "'";
        row = row.replace("<tr", tag);
        $($tbody).prepend(row);
      // $("#addModal").modal("toggle");
      })
      .fail(function (error) {
        alert("error");
      // $("#addModal").modal("toggle");
      });
      $("#addModal").modal("toggle");
  });
});


// import file
$(".importFile").click(function (e) {
  $("#importModal .saveBtnImport").click(function () {
    console.log('click')
    var fd = new FormData();
    var file = $("#importModal #customFile")[0].files;
    console.log('file:', file);
    console.log('file0: ', file[0]);
    var url = "http://127.0.0.1:5000/api/product/upload/";
    if (file.length > 0) {
      // console.log('file', file);
      fd.append('file', file[0]);
      // console.log(typeof file[0]);
      // console.log(file[0]);
      // console.log('fd', fd);
      // console.log(fd.getAll('file'));
      $.ajax({
        url: url,
        data: fd,
        method: "POST",
        contentType: false,
        processData: false,
        success: function (resp) {
          if (resp != 0) {
            alert("File uploaded");
            // console.log('file');
            $("#importModal").modal("toggle");
          } else {
            alert("File not uploaded");
            // console.log('no file')
          }
        },
      });
    } else {
      alert('Please select a file.');
    }
  });
});
