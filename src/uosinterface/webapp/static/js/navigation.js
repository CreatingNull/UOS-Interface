// When the user scrolls the page check if navbar needs to stick.
window.onscroll = function () {
  stickNavbar();
};

// When the page loads load device connection if persisted.
window.onload = function () {
  getPersistedDeviceSelection();
};

// Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon.
function dynamicNavigation() {
  let nav = document.getElementById("top-navigation");
  if (nav.classList.contains("responsive")) {
    nav.classList.remove("responsive");
  } else {
    nav.classList.add("responsive");
  }
}

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position.
function stickNavbar() {
  let navbar = document.getElementById("top-navigation"); // Get the navbar
  let stickyHeight = navbar.offsetTop; // Get the offset position of the navbar
  if (window.pageYOffset > stickyHeight) {
    navbar.classList.add("sticky");
  } else {
    navbar.classList.remove("sticky");
  }
}

// takes the currently selected navbar connection and writes this as the device connection form field.
function getSelectedConnection() {
  let sel = document.getElementById("device-select");
  document.getElementById("form-device-connection").value =
    sel.options[sel.selectedIndex].value;
}

// Uses javascript local storage to ensure device selection in nonvolatile over the session.
function persistDeviceSelection() {
  let sel = document.getElementById("device-select");
  window.localStorage.setItem(
    "device-selection",
    sel.options[sel.selectedIndex].value
  );
}

// Returns the previous device selection if it has been persisted.
function getPersistedDeviceSelection() {
  if (window.localStorage.getItem("device-selection") !== null) {
    let sel = document.getElementById("device-select");
    for (let i = 0; i < sel.options.length; i++) {
      if (
        sel.options[i].value === window.localStorage.getItem("device-selection")
      ) {
        sel.options[i].setAttribute("selected", "");
      } else if (sel.options[i].hasAttribute("selected")) {
        sel.options[i].removeAttribute("selected");
      }
    }
  }
}
