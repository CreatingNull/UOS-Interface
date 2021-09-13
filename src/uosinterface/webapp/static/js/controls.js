/** Add event listeners to elements on page load. */
window.addEventListener('load', function () {
  // Add spinner behaviour to tagged buttons.
  document
    .querySelectorAll('.control-numeric-spinner-right')
    .forEach((rightButton) =>
      rightButton.addEventListener(
        'click',
        function (event) {
          incrementSpinner(event, false);
        },
        false,
      ),
    );
  document
    .querySelectorAll('.control-numeric-spinner-left')
    .forEach((leftButton) =>
      leftButton.addEventListener(
        'click',
        function (event) {
          incrementSpinner(event, true);
        },
        false,
      ),
    );
});

/**
 * Increment Decrement Spinner.
 * @param {Event} event Single button object in the spinner.
 * @param {boolean} decrement Set if incrementing down.
 * */
function incrementSpinner(event, decrement) {
  const inputElement =
    event.target.parentElement.getElementsByTagName('input')[0];
  const limitLow = inputElement.dataset.limitLow;
  const limitHigh = inputElement.dataset.limitHigh;
  let value = Math.round(parseFloat(inputElement.value));
  if (decrement && value > limitLow) value--;
  else if (!decrement && value < limitHigh) value++;
  inputElement.value = value.toString();
}

/**
 * Toggles the class on a switch control.
 * @param {object} inputElement The switch input field element.
 */
function toggleSwitch(inputElement) {
  if (inputElement.classList.contains('active')) {
    inputElement.classList.remove('active');
  } else {
    inputElement.classList.add('active');
  }
}
