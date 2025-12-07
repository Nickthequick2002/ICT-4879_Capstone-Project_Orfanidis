/** This script controls the small profile dropdown 
 * that exists in the navbar, toggles the profile icon when clicked
 * and closes the menu when clicking anywhere else
 */

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("profileToggle");
  const menu = document.getElementById("profileMenu");

  if (toggle && menu) {

    // Toggle the dropdown visibility
    toggle.addEventListener("click", (e) => {
      e.stopPropagation(); // Prevents the triggering of the window click listener
      menu.classList.toggle("show"); //Show or hide the dropdown menu
    });

    // Clicking anywhere else closes the dropdown menu
    window.addEventListener("click", () => {
      menu.classList.remove("show");
    });
  }
});