/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
function dynamicNavigation() {
  var nav = document.getElementById("top-navigation");
  if (nav.className === "top-nav") {
    nav.className += " responsive";
  } else {
    nav.className = "top-nav";
  }
}
