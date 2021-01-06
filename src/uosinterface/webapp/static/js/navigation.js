/** When the user scrolls the page check if navbar needs to stick. */
window.onscroll = function () {
  stickNavbar();
};

/** When the page loads load device connection if persisted. */
window.onload = function () {
  getPersistedDeviceSelection();
};

/** Toggles the responsive class on nav when user clicks on icon. */
function dynamicNavigation() {
  const nav = document.getElementById('top-navigation');
  if (nav.classList.contains('responsive')) {
    nav.classList.remove('responsive');
  } else {
    nav.classList.add('responsive');
  }
}

/** Adds the sticky class once scroll passes threshold. */
function stickNavbar() {
  const navbar = document.getElementById('top-navigation'); // Get the navbar
  const stickyHeight = navbar.offsetTop; // Get the nav offset position
  if (window.pageYOffset > stickyHeight) {
    navbar.classList.add('sticky');
  } else {
    navbar.classList.remove('sticky');
  }
}

/** Writes currently selected connection to device connection form field. */
function getSelectedConnection() {
  const sel = document.getElementById('device-select');
  document.getElementById('form-device-connection').value =
    sel.options[sel.selectedIndex].value;
}

/** Saves device selection in nonvolatile location for the session. */
function persistDeviceSelection() {
  const sel = document.getElementById('device-select');
  window.localStorage.setItem(
    'device-selection',
    sel.options[sel.selectedIndex].value,
  );
}

/** Returns the previous device selection if it has been persisted. */
function getPersistedDeviceSelection() {
  if (window.localStorage.getItem('device-selection') !== null) {
    const sel = document.getElementById('device-select');
    for (let i = 0; i < sel.options.length; i++) {
      if (
        sel.options[i].value === window.localStorage.getItem('device-selection')
      ) {
        sel.options[i].setAttribute('selected', '');
      } else if (sel.options[i].hasAttribute('selected')) {
        sel.options[i].removeAttribute('selected');
      }
    }
  }
}

/** Go to tab by name */
function switchTab(tab) {
  let tabbedPane = tab.parentElement;
  let tabs = tabbedPane.getElementsByClassName('tab-nav-links');
  for (let i = 0; i < tabs.length; i++) {
    if (tabs[i] === tab && !tabs[i].classList.contains('active')) {
      tabs[i].classList.add('active');
    } else if (tabs[i] !== tab && tabs[i].classList.contains('active')) {
      tabs[i].classList.remove('active');
    }
  }
}
