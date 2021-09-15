/** Add event listeners to elements on page load. */
window.addEventListener('load', function () {
  // Add switch tab event listeners to any defined tab buttons.
  document
    .querySelectorAll('.tab-nav-links')
    .forEach((tabButtons) =>
      tabButtons.addEventListener('click', switchTab, false),
    );
  // Make the navbar sticky on the page.
  window.onscroll = stickNavbar;
  // Dynamic navigation event listener for mobile navigation
  document
    .querySelector('.nav.top-nav.icon')
    .addEventListener('click', dynamicNavigation, false);
  // Persist Device Selections
  document
    .querySelector('#device-select')
    .addEventListener('click', persistDeviceSelection, false);
});

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

/** Saves device selection in nonvolatile location for the session. */
function persistDeviceSelection() {
  const sel = document.getElementById('device-select');
  window.localStorage.setItem(
    'device-selection',
    sel.options[sel.selectedIndex].value,
  );
}

/**
 * Go to tab by name, added to buttons with tab-nav-links *
 * @param {Event} event object for determining the target of the switch Tab action.
 */
function switchTab(event) {
  const tabHeaders =
    event.target.parentElement.getElementsByClassName('tab-nav-links');
  const tabs =
    event.target.parentElement.parentElement.getElementsByClassName(
      'tab-nav-content',
    );
  for (let i = 0; i < tabHeaders.length; i++) {
    if (
      tabHeaders[i] === event.target &&
      !tabHeaders[i].classList.contains('active')
    ) {
      tabHeaders[i].classList.add('active');
      tabs[i].classList.add('active');
    } else if (
      tabHeaders[i] !== event.target &&
      tabHeaders[i].classList.contains('active')
    ) {
      tabHeaders[i].classList.remove('active');
      tabs[i].classList.remove('active');
    }
  }
}
