window.addEventListener("scroll", updateScrollElements);
updateScrollElements();

function updateScrollElements() {
  const isScrolled =
    document.body.scrollTop > 10 ||
    document.documentElement.scrollTop > 10;

  setDisplay("f-to-top-button", isScrolled, "flex");
  setDisplay("cover-logo", !isScrolled);
  setDisplay("vigo-triangle", !isScrolled);
}

function setDisplay(elementId, visible, displayType = "block") {
  const element = document.getElementById(elementId);

  if (element) {
    element.style.display = visible ? displayType : "none";
  }
}

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
} 