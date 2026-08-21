window.addEventListener("scroll", updateScrollElements);

function updateScrollElements() {
  const isScrolled =
    document.body.scrollTop > 10 ||
    document.documentElement.scrollTop > 10;

  setDisplay("f-to-top-button", isScrolled);
  setDisplay("cover-logo", !isScrolled);
  setDisplay("vigo-triangle", !isScrolled);
}

function setDisplay(elementId, visible) {
  const element = document.getElementById(elementId);

  if (element) {
    element.style.display = visible ? "block" : "none";
  }
}

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
} 