/** This script makes sure that both the sign up modal and the log in modal open.
 * This javascript is only used when the user is viewing the page as a visitor
 * and presses the get full access button of the programs. 
 */

document.addEventListener("DOMContentLoaded", function () {

    // Get main modal elements
    const authModal   = document.getElementById("authRequiredModal");
    const authContent = authModal?.querySelector(".auth-modal-content");

    // Get buttons inside the modal
    const signupBtn   = document.getElementById("authSignupBtn");
    const loginBtn    = document.getElementById("authLoginBtn");

    // Get the login and signup modals
    const loginModal  = document.getElementById("loginModal");
    const signupModal = document.getElementById("signupModal");

    if (!authModal) return; // Just a safety check


    // Open auth modal when pressing "Get Full Access"
    document.querySelectorAll(".get-full-access").forEach(btn => {
        btn.addEventListener("click", function (event) {
            event.preventDefault();
            authModal.style.display = "flex";
            document.body.style.overflow = "hidden";   // freeze page scroll
        });
    });

    // Close modal when clicking outside
    authModal.addEventListener("click", (e) => {
        if (e.target === authModal) {
            authModal.style.display = "none";
            document.body.style.overflow = "auto"; // restore scroll
        }
    });

    // Prevent closing when clicking inside the modal box
    if (authContent) {
        authContent.addEventListener("click", (e) => {
            e.stopPropagation();
        });
    }

    // Open signup modal
    if (signupBtn && signupModal) {
        signupBtn.addEventListener("click", (e) => {
            e.stopPropagation(); // Protect from bubbling
            authModal.style.display = "none"; // Close auth modal
            signupModal.style.display = "flex"; // Show signup modal
            document.body.style.overflow = "hidden"; // Lock scroll
        });
    }

    // Open login modal
    if (loginBtn && loginModal) {
        loginBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            authModal.style.display = "none";
            loginModal.style.display = "flex";
            document.body.style.overflow = "hidden";
        });
    }

});
