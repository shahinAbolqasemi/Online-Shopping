var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

var counter = 0;
function buyCounter(event) {
  counter += 1
  document.getElementById("buyCount").innerHTML = counter ;
}