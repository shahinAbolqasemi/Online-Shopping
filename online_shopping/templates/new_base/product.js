var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


var counter = 0;
var z = document.getElementById("number");
function buyCounter() {
  counter += z
  document.getElementById("buyCount").innerHTML = counter ;
  document.getElementById("number").value = 0;
}

function openImg(imgName) {
    var i, x;
    x = document.getElementsByClassName("picture");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    document.getElementById(imgName).style.display = "block";
  }
  