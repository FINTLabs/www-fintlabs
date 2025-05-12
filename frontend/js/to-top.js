window.onscroll = function () {
  scrollFunction()
};

function scrollFunction() {
  console.log(document.body.scrollTop)
  console.log(document.documentElement.scrollTop)
  if (document.body.scrollTop > 10 || document.documentElement.scrollTop > 10) {
    document.getElementById("f-to-top-button").style.display = "block";
    document.getElementById("cover-logo").style.display = "none";
    document.getElementById("vigo-triangle").style.display = "none";
  } else {
    document.getElementById("cover-logo").style.display = "block";
    document.getElementById("vigo-triangle").style.display = "block";
    document.getElementById("f-to-top-button").style.display = "none";

  }
}

// When the user clicks on the button, scroll to the top of the document
function scrollToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
