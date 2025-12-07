/** Handles the behavior of the "Upgrade to Member" modal.
 * If the user is not logged in it gets a small popup reminder that he should log in or sign up
 * If the user is logged in, but not member, it opens the upgrade modal
 */

document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("upgradeModal");
  const lockedButtons = document.querySelectorAll(".locked-program .btn-get-access");
  const authPopup = document.getElementById("authPopup");

  lockedButtons.forEach(button => {
    button.addEventListener("click", function (e) {

      // Does not open the modal if the user is not authenticated
      if (button.classList.contains("not-auth-btn")) {
        e.preventDefault();

        authPopup.style.display = "block";

        // Hide opoup after 2.5s
        setTimeout(() => {
          authPopup.style.display = "none";
        }, 2500);
        return;
      }

      // Opens the modal if user is authenticated
      e.preventDefault();
      modal.style.display = "flex";
      document.body.style.overflow = "hidden";
    });
  });

  // Close modal when clicking outside
  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
      document.body.style.overflow = "auto";
    }
  });
});
