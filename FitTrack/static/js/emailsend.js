/** This script handles the contact form submission
 * prevents the default page from reloading after the submission,
 * send an automated email to the user and shows a popup message
 * depending on the result
 */

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("contactForm");
  const submitButton = document.getElementById("submit-button");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();  // Prevent full page refresh
  
    // Disable the button  to prevent multiple submissions
    submitButton.disabled = true;
    submitButton.textContent = "Sending...";

    const formData = new FormData(form);

    try {
      // Empty string equals to the submition of the current URL
      const response = await fetch("", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        // Success message for the user
        Swal.fire({
          icon: "success",
          title: "Message sent!",
          text: "We are going to respond within 24 hours.",
          confirmButtonColor: "#ffa94d",
      });

        form.reset(); // Clear all the fields after the successful send
      } else {
        // Server response when an error is occured 
        Swal.fire({
          icon: "error",
          title: "Oops!",
          text: "Something went wrong. Please try again later.",
        });
      }
    } catch (error) {
      // Network or connection error
      Swal.fire({
        icon: "error",
        title: "Network Error",
        text: "Please check your internet connection and try again.",
      });
      console.error("Error:", error);
    } finally {
      // Re-enable button regardless of the success or failure
      submitButton.disabled = false;
      submitButton.textContent = "Send Message";
    }
  });
});