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

    // Standard django CSRF  function to read and return the value of a requested cookie
    const csrftoken = getCookie("csrftoken");

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
            
            // Show a small popup confirmation message
            const popup = document.getElementById("password-popup");
            popup.style.display = "block";

            // Hide the popup message after 2 seconds
            setTimeout(() => popup.style.display = "none", 2000);

            // Clears the fields after a successfull password change
            document.getElementById("current-password").value = "";
            document.getElementById("new-password").value = "";
            document.getElementById("confirm-password").value = "";
        } else {

            // Simple alert from django
            alert(data.error);
        }
    })
    .catch(err => console.error("Fetch error:", err));
}

// Updates the training preferences (focus, goal, exercise type)
function updatePreferences() {

    // Read the selected values from the dropdowns
    const focus = document.getElementById("pref-focus").value;
    const goal = document.getElementById("pref-goal").value;
    const exercise = document.getElementById("pref-exercise").value;

    // Standard Django CSRF token (needed for POST requests)
    const csrftoken = getCookie("csrftoken");

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

            // Show the green confirmation popup
            const popup = document.getElementById("preferences-popup");
            popup.style.display = "block";

            // Hide popup after 2 seconds (same behavior as username/password)
            setTimeout(() => {
                popup.style.display = "none";
            }, 2000);

        } else {
            // Backend returned an error
            alert(data.error || "Could not update preferences.");
        }
    })
    .catch(err => {
        // Fallback error message for network/server issues
        console.error("Update preferences error:", err);
        alert("Something went wrong. Please try again.");
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



