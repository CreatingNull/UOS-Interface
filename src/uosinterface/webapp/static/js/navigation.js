/** When the user scrolls the page check if navbar needs to stick. */
window.onscroll = function () {
  stickNavbar();
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

window.addEventListener('load', function (event) {
  // Add switch tab event listeners to any defined tab buttons.
  let tabButtons = document.getElementsByClassName('tab-nav-links');
  for (let i = 0; i < tabButtons.length; i++) {
    tabButtons[i].addEventListener('click', switchTab, false);
  }

  /** Go to tab by name, added to buttons with tab-nav-links */
  function switchTab(event) {
    const tabHeaders = event.target.parentElement.getElementsByClassName(
      'tab-nav-links',
    );
    const tabs = event.target.parentElement.parentElement.getElementsByClassName(
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
});
