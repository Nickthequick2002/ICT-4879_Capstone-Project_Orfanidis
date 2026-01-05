/** This script controll all the signup modal behaviors.\
 * It opens and closes the signup modal 
 * and handles all the functionality inside it
 */

document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("signupModal");
  const openBtn = document.getElementById("openSignup");
  const closeBtn = document.getElementById("closeSignup");
  const signupForm = document.getElementById("signupForm");
  const errorDiv = document.getElementById("signupError");

  // Opens signup modal
  if (openBtn) {
    openBtn.addEventListener("click", (e) => {
      e.preventDefault();
      modal.style.display = "flex";
      document.body.style.overflow = "hidden"; // Lock scroll owhile modal is open
    });
  }

  // Close signup modal
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      modal.style.display = "none";
      document.body.style.overflow = "auto"; //  Lock scroll owhile modal is open
    });
  }

  // Close when clicked outside the modal
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
      document.body.style.overflow = "auto";
    }
  });

  // Password visibility toggle
  // Two fields, password and confim password
  const toggles = [
    { icon: "togglePassword1", input: "passwordInput1" },
    { icon: "togglePassword2", input: "passwordInput2" },
  ];

  toggles.forEach(({ icon, input }) => {
    const toggle = document.getElementById(icon);
    const field = document.getElementById(input);

    if (toggle && field) {
      toggle.addEventListener("click", () => {

        // Swap between password and text input types
        const type =
        field.getAttribute("type") === "password" ? "text" : "password";
        field.setAttribute("type", type);

        // Update icons visually
        toggle.classList.toggle("fa-eye");
        toggle.classList.toggle("fa-eye-slash");
      });
    }
  });

  // Handles the signup form submission=
  if (signupForm) {
    signupForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      const formData = new FormData(this);

      try {
        const response = await fetch("/accounts/signup/", {
          method: "POST",
          body: formData,
          credentials: "same-origin" // Ensures Django cookies/CSRF work
        });
        const data = await response.json();

        if (data.success) {
          modal.style.display = "none";
          document.body.style.overflow = "auto";
          this.reset();

          // Refresh to instantly update navbar
          window.location.reload();
        } else {
          // Show backend error message inside modal
          errorDiv.textContent = data.error;
        }
      } catch (err) {
        // Generic catch-all fallback
        errorDiv.textContent = "Something went wrong. Please try again.";
      }
    });
  }
});
