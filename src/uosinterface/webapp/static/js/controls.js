/**
 * Increment Decrement Spinner.
 * @param {object} buttonElement Single button object in the spinner.
 * @param {boolean} decrement Boolean does button decrease value.
 * @param {number} limit Sets the bound for the count.
 * */
function incrementSpinner(buttonElement, decrement, limit) {
  const inputElement = buttonElement.parentElement.getElementsByTagName(
    'input',
  )[0];
  let value = Math.round(parseFloat(inputElement.value));
  if (decrement && value > limit) value--;
  else if (!decrement && value < limit) value++;
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
