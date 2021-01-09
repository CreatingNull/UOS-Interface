/** When the page loads load device connection if persisted. */
window.onload = function () {
  getPersistedDeviceSelection();
};

/**
 * Writes currently selected connection to device connection form field.
 * @param form_id {String} id of the element to populate onclick.
 */
function getSelectedConnection(form_id) {
  const sel = document.getElementById('device-select');
  document.getElementById(form_id).value = sel.options[sel.selectedIndex].value;
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
