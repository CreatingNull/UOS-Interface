/** When the page runs pre-emptive code. */
window.onload = function () {
  getPersistedDeviceSelection(); // device selection populates.
  setCloseableDivs(); // adds event listeners for closable divs.
};

/** Set event listeners on all closable divs. */
function setCloseableDivs() {
  const closableDivs = document.getElementsByClassName('close-pane');
  for (let i = 0; i < closableDivs.length; i++) {
    closableDivs[i].addEventListener('click', function (e) {
      if (!e.target.parentElement.classList.contains('close-pane-div')) {
        e.target.parentElement.classList.add('close-pane-div');
      }
    });
  }
}

/**
 * Writes currently selected connection to device connection form field.
 * @param {string} formId ID of the element to populate onclick.
 */
function getSelectedConnection(formId) {
  const sel = document.getElementById('device-select');
  document.getElementById(formId).value = sel.options[sel.selectedIndex].value;
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
