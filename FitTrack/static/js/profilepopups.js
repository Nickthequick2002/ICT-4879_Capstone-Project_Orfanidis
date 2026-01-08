/** This script handles the pop up message when the user changes username,
 * changes password and changes his preferences.
 */

function getCookie(name) {

    // Basic helper function to read the value of a given cookie
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();

            // Match the value of the CSRF token
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function changePassword() {

    // These are the three password inputs that the function uses
    const currentPassword = document.getElementById("current-password").value.trim();
    const newPassword = document.getElementById("new-password").value.trim();
    const confirmPassword = document.getElementById("confirm-password").value.trim();
    
    const btn = document.getElementById("update-password-btn");
    const originalText = btn.innerText;
    const originalClass = btn.className;

    // Standard django CSRF  function to read and return the value of a requested cookie
    const csrftoken = getCookie("csrftoken");

    btn.disabled = true;
    btn.innerText = "Updating...";

    fetch("/accounts/change-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            current_password: currentPassword,
            new_password: newPassword,
            confirm_password: confirmPassword
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response:", data); // Test during development to see if the function works

        if (data.success) {
            
            // Button Feedback
            btn.innerText = "Password Updated!";
            btn.className = "btn btn-success w-100 rounded-pill fw-bold shadow-sm"; 

            // Hide the popup message after 2 seconds
            setTimeout(() => {
                btn.innerText = originalText;
                btn.className = originalClass;
                btn.disabled = false;
            }, 2000);

            // Clears the fields after a successfull password change
            document.getElementById("current-password").value = "";
            document.getElementById("new-password").value = "";
            document.getElementById("confirm-password").value = "";
        } else {

            // Simple alert from django
            alert(data.error);
            btn.disabled = false;
            btn.innerText = originalText;
        }
    })
    .catch(err => {
        console.error("Fetch error:", err);
        btn.disabled = false;
        btn.innerText = originalText;
    });
}

// Updates the training preferences (focus, goal, exercise type)
function updatePreferences() {

    // Read the selected values from the dropdowns
    const focus = document.getElementById("pref-focus").value;
    const goal = document.getElementById("pref-goal").value;
    const exercise = document.getElementById("pref-exercise").value;
    
    // Get the Button for feedback
    const btn = document.getElementById("save-preferences-btn");
    const originalText = btn.innerText;
    const originalClass = btn.className;

    // Standard Django CSRF token (needed for POST requests)
    const csrftoken = getCookie("csrftoken");

    btn.disabled = true;
    btn.innerText = "Values Saving...";

    // Send the updated values to the backend
    fetch("/accounts/update-preferences/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            focus_body_part: focus,
            goal: goal,
            exercise_type: exercise
        })
    })
    .then(response => response.json())
    .then(data => {

        // If Django confirms the update was successful
        if (data.success) {

            // Button Success Feedback
            btn.innerText = "Saved!";
            btn.className = "btn btn-success rounded-pill w-100 fw-bold shadow-sm"; // Turn green
            
            // Revert after 2 seconds
            setTimeout(() => {
                btn.innerText = originalText;
                btn.className = originalClass;
                btn.disabled = false;
            }, 2000);

        } else {
            // Backend returned an error
            alert(data.error || "Could not update preferences.");
            btn.disabled = false;
            btn.innerText = originalText;
        }
    })
    .catch(err => {
        // Fallback error message for network/server issues
        console.error("Update preferences error:", err);
        alert("Something went wrong. Please try again.");
        btn.disabled = false;
        btn.innerText = originalText;
    });
}


// CSRF token for the helper function
// Small function to read a specific cookie value
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken'); // Grabs the CSRF token

// Function to change the username 
function changeUsername() {
    console.log("Button clicked!"); // Used during the development for debugging

    const newUsername = document.getElementById("new-username").value.trim();

    if (!newUsername) {
        alert("Please enter a username.");
        return;
    }

    console.log("Sending request...");

    fetch("/accounts/change-username/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken, // Required for Django POST requests
        },
        body: JSON.stringify({ username: newUsername })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Response:", data); // Used during the development for debugging

        if (data.success) {
            
            // Update displayed username in the UI
            document.getElementById("current-username").innerText = newUsername;

            // Show confirmation popup
            const popup = document.getElementById("username-popup");
            popup.style.display = "block";
            setTimeout(() => popup.style.display = "none", 2000);

            // Clear input field
            document.getElementById("new-username").value = "";
        } else {
            alert(data.error);
        }
    })
    .catch(err => console.error("Fetch error:", err));
}





// Update all account details (First/Last/Email/Username)
function updateAccountDetails() {
    const firstName = document.getElementById('account-first-name').value.trim();
    const lastName = document.getElementById('account-last-name').value.trim();
    const email = document.getElementById('account-email').value.trim();
    const username = document.getElementById('account-username').value.trim();

    if (!username || !email) {
        alert('Username and Email are required.');
        return;
    }

    fetch('/accounts/update-details/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            email: email,
            username: username
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Success Feedback
            const btn = document.getElementById("save-account-btn");
            const originalText = btn.innerText;
            const originalClass = btn.className;

            btn.innerText = "Saved!";
            btn.className = "btn btn-success rounded-pill px-4"; // Turn green
            btn.disabled = true;

            setTimeout(() => {
                btn.innerText = originalText;
                btn.className = originalClass; // Revert
                btn.disabled = false;
            }, 2000);
            
            // Update displayed username if changed
            const welcomeMsg = document.getElementById("welcome-message");
            if (welcomeMsg) {
                welcomeMsg.innerText = "Welcome back, " + username + "!";
            }
        } else {
            alert(data.error);
        }
    })
    .catch(err => console.error('Error:', err));
}

// Upload Profile Picture via AJAX
function uploadPfp(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById("pfp-input");
    const file = fileInput.files[0];
    
    if (!file) {
        alert("Please select an image file.");
        return;
    }

    const formData = new FormData();
    formData.append("profile_picture", file);

    fetch("/accounts/update-pfp-ajax/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Update images
            const headerImg = document.getElementById("profile-header-img");
            const settingsImg = document.getElementById("settings-pfp-img");

            // Add a timestamp to bypass cache if URL is same
            const newSrc = data.image_url; 

            if (headerImg) headerImg.src = newSrc;
            if (settingsImg) settingsImg.src = newSrc;

            // Button Feedback
            const btn = document.getElementById("pfp-btn");
            const originalText = btn.innerText;
            const originalClass = btn.className;

            btn.innerText = "Saved!";
            btn.className = "btn btn-success rounded-pill btn-sm mt-3"; 
            btn.disabled = true;

            setTimeout(() => {
                btn.innerText = originalText;
                btn.className = originalClass; 
                btn.disabled = false;
                fileInput.value = ""; 
            }, 2000);

        } else {
            alert(data.error || "Upload failed.");
        }
    })
    .catch(err => console.error("Error:", err));
}

// Testimonial AJAX Update
function updateTestimonialAjax() {
    const msgInput = document.getElementById("testimonial-msg");
    const message = msgInput.value.trim();
    
    if (!message) {
        alert("Message cannot be empty.");
        return;
    }

    fetch("/accounts/edit-testimonial-ajax/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Button Feedback
            const btn = document.getElementById("update-testimonial-btn");
            const originalText = btn.innerText;
            const originalClass = btn.className;

            btn.innerText = "Saved!";
            btn.className = "btn btn-success rounded-pill px-4 mx-2"; 
            btn.disabled = true;

            setTimeout(() => {
                btn.innerText = originalText;
                btn.className = originalClass; 
                btn.disabled = false;
            }, 2000);
        } else {
            alert(data.error);
        }
    })
    .catch(err => console.error("Error:", err));
}

// Testimonial AJAX Submit
function submitTestimonialAjax() {
    const msgInput = document.getElementById("submit-testimonial-msg");
    const message = msgInput.value.trim();
    
    if (!message) {
        alert("Share your story first!");
        return;
    }

    fetch("/accounts/submit-testimonial-ajax/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const btn = document.getElementById("submit-testimonial-btn");
            btn.innerText = "Saved!";
            btn.className = "btn btn-success rounded-pill px-4"; 
            btn.disabled = true;

            setTimeout(() => {
                // Switch to Update/Delete mode
                msgInput.id = "testimonial-msg"; // Rename input
                
                const form = document.getElementById("submit-testimonial-form");
                if (form) {
                    form.id = "testimonial-form";
                    form.action = "/accounts/profile/testimonial/edit/"; 
                }
                
                // Rename Container and Replace Buttons
                const container = document.getElementById("submit-btn-container");
                if (container) {
                    container.id = "update-btn-container";
                    container.innerHTML = `
                         <button id="update-testimonial-btn" type="button" onclick="updateTestimonialAjax()" class="btn btn-outline-brand-orange rounded-pill px-4 mx-2">Update</button>
                         <button id="delete-testimonial-btn" type="button" onclick="deleteTestimonialAjax()" class="btn btn-outline-danger rounded-pill px-4 mx-2">Delete</button>
                    `;
                }
            }, 1000);
        } else {
            alert(data.error);
        }
    })
    .catch(err => console.error("Error:", err));
}

// Testimonial AJAX Delete
function deleteTestimonialAjax() {
    if (!confirm("Are you sure you want to delete your testimonial?")) {
        return;
    }

    fetch("/accounts/delete-testimonial-ajax/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const btn = document.getElementById("delete-testimonial-btn");
            btn.innerText = "Deleted!";
            btn.className = "btn btn-danger rounded-pill px-4 mx-2";
            btn.disabled = true;

            setTimeout(() => {
                // Switch back to Submit mode
                const msgInput = document.getElementById("testimonial-msg");
                if (msgInput) {
                    msgInput.value = "";
                    msgInput.placeholder = "Share your story...";
                    msgInput.id = "submit-testimonial-msg";
                }

                const form = document.getElementById("testimonial-form");
                if (form) {
                    form.id = "submit-testimonial-form";
                    form.action = "/accounts/profile/testimonial/submit/";
                }

                const container = document.getElementById("update-btn-container");
                if (container) {
                    container.id = "submit-btn-container";
                    container.innerHTML = `<button id="submit-testimonial-btn" type="button" onclick="submitTestimonialAjax()" class="btn btn-outline-brand-orange rounded-pill px-4">Submit</button>`;
                }
            }, 1000);
        } else {
            alert(data.error || "Delete failed.");
        }
    })
    .catch(err => console.error("Error:", err));
}
