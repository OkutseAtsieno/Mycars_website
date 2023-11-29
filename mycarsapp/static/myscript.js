$(".plus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var enl = this.parentNode.children[2];
  console.log("pid-", id);

  $.ajax({
    type: "GET",
    url: "/pluscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
        console.log("data=", data);
        enl.innerText = data.quantity
        document.getElementById("amount").innerText = data.amount
        document.getElementById("totalamount").innerText = data.totalamount
        
    },
  });
});

$(".minus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var enl = this.parentNode.children[2];
  console.log("pid-", id);

  $.ajax({
    type: "GET",
    url: "/minuscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      console.log("data=", data);
      enl.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
    },
  });
});

$(".remove-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var enl = this.parentNode.children[2];
  console.log("pid-", id);

  $.ajax({
    type: "GET",
    url: "/removecart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      console.log("data=", data);
      enl.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
        document.getElementById("totalamount").innerText = data.totalamount;
        enl.parentNode.parentNode.parentNode.parentNode.remove()
        
    },
  });
});

$(".plus-wishlist").click(function () {
  var id = $(this).attr("pid").toString();
  
  $.ajax({
    type: "GET",
    url: "/pluswishlist",
    data: {
      prod_id: id,
    },
    success: function (data) {
      //alert data .message
      window.location.href='http://localhost:8000/product-detail/$(id'
    },
  });
});

$(".minus-wishlist").click(function () {
  var id = $(this).attr("pid").toString();

  $.ajax({
    type: "GET",
    url: "/minuswishlist",
    data: {
      prod_id: id,
    },
    success: function (data) {
      //alert data .message
      window.location.href = "http://localhost:8000/product-detail/$(id";
    },
  });
});

