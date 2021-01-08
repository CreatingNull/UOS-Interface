/**
 * Increment Decrement Spinner.
 * @param {object} button_element Single button object in the spinner.
 * @param {boolean} decrement Boolean does button decrease value.
 * @param {limit} limit Sets the bound for the count.
 * */
function incrementSpinner(button_element, decrement, limit) {
  const inputElement = button_element.parentElement.getElementsByTagName(
    'input',
  )[0];
  let value = Math.round(parseFloat(inputElement.value));
  if (decrement && value > limit) value--;
  else if (!decrement && value < limit) value++;
  inputElement.value = value.toString();
}

/**
 * Toggles the class on a switch control.
 * @param input_element The switch input field element.
 */
function toggleSwitch(input_element) {
  if (input_element.classList.contains('active')) {
    input_element.classList.remove('active');
  } else {
    input_element.classList.add('active');
  }
}
