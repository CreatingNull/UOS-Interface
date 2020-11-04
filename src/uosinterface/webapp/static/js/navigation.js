// When the user scrolls the page check if navbar needs to stick.
window.onscroll = function () {
  stickNavbar();
};

// Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon.
function dynamicNavigation() {
  var nav = document.getElementById("top-navigation");
  if (nav.classList.contains("responsive")) {
    nav.classList.remove("responsive");
  } else {
    nav.classList.add("responsive");
  }
}

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position.
function stickNavbar() {
  var navbar = document.getElementById("top-navigation"); // Get the navbar
  var stickyHeight = navbar.offsetTop; // Get the offset position of the navbar
  if (window.pageYOffset > stickyHeight) {
    navbar.classList.add("sticky");
  } else {
    navbar.classList.remove("sticky");
  }
}

// takes the currently selected navbar connection and writes this as the device connection form field.
function getSelectedConnection() {
  var sel = document.getElementById("device-select");
  document.getElementById("form-device-connection").value =
    sel.options[sel.selectedIndex].value;
}
