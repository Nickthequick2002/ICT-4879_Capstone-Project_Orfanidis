/** This script controls the login modal behavior,
 * opens the modal from multiple trrigers,
 * locks the outside scolling when the modal is opened,.
 * allows the view of the given password and displays error messages
 */

document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("loginModal");
  const closeBtn = document.getElementById("closeModal");
  const loginForm = document.getElementById("loginForm");
  const errorDiv = document.getElementById("loginError");
  const openBtn = document.getElementById("openLogin");
  const openBtnMain = document.getElementById("openLoginMain");

  
  // Opens the login modal when clicking the login icon in the navbar
  if (openBtn) {
    openBtn.addEventListener("click", (e) => {
      e.preventDefault();
      modal.style.display = "flex";
      document.body.style.overflow = "hidden"; // Locks scroll while in the modal
    });
  }

  // Open modal from the main "Continue your journey" button
  if (openBtnMain) {
    openBtnMain.addEventListener("click", (e) => {
      e.preventDefault();
      modal.style.display = "flex";
      document.body.style.overflow = "hidden"; // Locks scroll while in the modal
    });
  }

  // Closes the login modal when the user presses the x button
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      modal.style.display = "none";
      document.body.style.overflow = "auto"; // Unlock the scolling
    });
  }

  // Closes the login modal when the user clicks outside
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
      document.body.style.overflow = "auto"; // Unlock the scolling
    }
  });

  // Submits the login form
  document.addEventListener("submit", async function (e) {
    const form = e.target;
    if (form.id !== "loginForm") return; // Handles only the login form

    e.preventDefault();
    const formData = new FormData(form);

    try {
      // Django login endpoint
      const response = await fetch("/accounts/login/", {
        method: "POST",
        body: formData,
        credentials: "same-origin", // Ensure that CSRF cookies work
      });

      const data = await response.json();

      if (data.success) {

        // Closes modal and resets the scolling
        modal.style.display = "none";
        document.body.style.overflow = "auto";
        form.reset();

        // Instant refresh to update the UI
        window.location.reload();
      } else {

        // Print any backend erros messages
        if (errorDiv)
          errorDiv.textContent = data.error || "Invalid credentials";
      }
    } catch (err) {

      // Print any network or server issues
      if (errorDiv)
        errorDiv.textContent = "Something went wrong. Please try again.";
    }
  });

  // Toggles the password visibility
  const togglePassword = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("passwordInput");

  if (togglePassword && passwordInput) {
    togglePassword.addEventListener("click", () => {

      // Switch between password and text input type vice versa
      const type =
      passwordInput.getAttribute("type") === "password" ? "text" : "password";
      passwordInput.setAttribute("type", type);

      // Swap icons (the eye becomes eye-slash and vice versa)
      togglePassword.classList.toggle("fa-eye");
      togglePassword.classList.toggle("fa-eye-slash");
    });
  }
});
