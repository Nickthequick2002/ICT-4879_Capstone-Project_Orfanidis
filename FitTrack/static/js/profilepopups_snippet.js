
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

            // Add a timestamp to bypass cache if URL is same (though Django changes URL usually if name changes, but overwriting might not)
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
                // Clear input
                fileInput.value = ""; 
            }, 2000);

        } else {
            alert(data.error || "Upload failed.");
        }
    })
    .catch(err => console.error("Error:", err));
}
