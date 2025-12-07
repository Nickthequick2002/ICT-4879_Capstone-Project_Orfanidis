/** Saves and restores scoll position on the "My cals" page.
 * When the user adds a food, the page refreshes and goes 
 * instantly to the section the user was in
 */

document.addEventListener("DOMContentLoaded", function () {

  // Checks if there is a saved scroll position from previous action
  const savedScrollY = sessionStorage.getItem("scrollY");
  if (savedScrollY !== null) {
    // Restore the rpevious vertical scrool position
    window.scrollTo(0, parseFloat(savedScrollY));

    // Clear the stored value and only restore once
    sessionStorage.removeItem("scrollY");
  }

  // Before navigatin, the current scroll position is saved
  document.querySelectorAll("form, a.remove-btn").forEach(el => {
    el.addEventListener("click", () => {
      sessionStorage.setItem("scrollY", window.scrollY);
    });
  });
});