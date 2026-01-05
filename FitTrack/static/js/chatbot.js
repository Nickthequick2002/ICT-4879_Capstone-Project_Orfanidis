/**
 * FitTrack Chatbot powered with AI
 * Frontend handles ONLY UI.
 * All intelligence lives in the backend.
 */

document.addEventListener("DOMContentLoaded", () => {


    // DOM elements
    const bubble = document.getElementById("ft-chatbot-toggle");
    const chatWindow = document.getElementById("ft-chatbot-window");
    const closeBtn = document.getElementById("ft-chat-close");

    const input = document.getElementById("ft-chat-text");
    const sendBtn = document.getElementById("ft-chat-send");
    const chatBody = document.getElementById("ft-chat-body");

    // Safety check
    if (!bubble || !chatWindow || !closeBtn || !input || !sendBtn || !chatBody) return;

    // Open chat
    bubble.addEventListener("click", () => {
        chatWindow.classList.add("active");
        bubble.classList.add("hidden");
        input.focus();
        greetOnce();
    });

    // Close chat
    closeBtn.addEventListener("click", () => {
        chatWindow.classList.remove("active");
        bubble.classList.remove("hidden");
    });

    // Add user message
    function addUserMessage(text) {
        const msg = document.createElement("div");
        msg.classList.add("ft-msg", "user");
        msg.textContent = text;
        chatBody.appendChild(msg);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Add bot message
    function addBotMessage(text) {
        const msg = document.createElement("div");
        msg.classList.add("ft-msg", "bot");
        msg.textContent = text;
        chatBody.appendChild(msg);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    let typingIndicator = null;

    function showTyping() {
        if (typingIndicator) return;

        typingIndicator = document.createElement("div");
        typingIndicator.classList.add("ft-msg", "bot", "typing");

        const span = document.createElement("span");
        const bubble = document.createElement("div");
        bubble.classList.add("typing-bubble");

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement("span");
            bubble.appendChild(dot);
        }

        typingIndicator.appendChild(bubble);

        typingIndicator.appendChild(span);
        chatBody.appendChild(typingIndicator);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function removeTyping() {
        if (typingIndicator) {
            typingIndicator.remove();
            typingIndicator = null;
        }
    }

    // Send message
    sendBtn.addEventListener("click", () => {
        const message = input.value.trim();
        if (!message) return;

        addUserMessage(message);
        input.value = "";

        sendToBackend(message);
    });

    // Enter key support
    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendBtn.click();
        }
    });

    // Backend call
    function sendToBackend(message) {
        showTyping();

        fetch("/chatbot/reply/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({ message })
        })
        .then(res => res.json())
        .then(data => {
            removeTyping();
            if (data.reply) {
                addBotMessage(data.reply);
            } else {
                addBotMessage("Sorry, I couldn’t answer that.");
            }
        })
        .catch(() => {
            removeTyping();
            addBotMessage("Something went wrong. Please try again.");
        });
    }

    // CSRF helper
    function getCSRFToken() {
        return document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1];
    }
});
