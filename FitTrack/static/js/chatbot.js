/** This script is used for the chatbot as it loads the intents json file,
 * handles the opening and the closing of the chat window,
 * makes the chatbot process the user's messages
 * and then respond based on the matching patterns
 */

document.addEventListener("DOMContentLoaded", () => {

    let hasGreeted = false; // Prevents the bot from greeting a second time
    let intents = []; // This holds all the loaded intents from the json file

    // Load intents.json
    fetch("/static/json/intents.json")
        .then(response => response.json())
        .then(data => {
            intents = data.intents;
            console.log("Intents loaded:", intents);
        })
        .catch(error => console.error("Error loading intents:", error)); // Using during the development to see if the functionality works properly

    // DOM elements in order to avoid repearted lookups
    const bubble = document.getElementById("ft-chatbot-toggle");
    const chatWindow = document.getElementById("ft-chatbot-window");
    const closeBtn = document.getElementById("ft-chat-close");

    const input = document.getElementById("ft-chat-text");
    const sendBtn = document.getElementById("ft-chat-send");
    const chatBody = document.getElementById("ft-chat-body");

    // If any critical element is missing, the script stops
    if (!bubble || !chatWindow || !closeBtn || !input || !sendBtn) return;

    // Open the chat window
    bubble.addEventListener("click", () => {
        chatWindow.classList.add("active");
        bubble.classList.add("hidden");
    });

    // Close the chat window
    closeBtn.addEventListener("click", () => {
        chatWindow.classList.remove("active");
        bubble.classList.remove("hidden");
    });

    // Adds user message to trhe chat window
    function addUserMessage(text) {
        const msg = document.createElement("div");
        msg.classList.add("ft-msg", "user");
        msg.textContent = text;
        chatBody.appendChild(msg);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Adds bot message to the chat window
    function addBotMessage(text) {
        const msg = document.createElement("div");
        msg.classList.add("ft-msg", "bot");
        msg.innerHTML = text;
        chatBody.appendChild(msg);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Sends message when the button is clicked
    sendBtn.addEventListener("click", () => {
        const message = input.value.trim();
        if (message === "") return;

        addUserMessage(message);
        processBotReply(message);
        input.value = "";
    });

    // Allow sending message by pressing the Enter key
    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendBtn.click();
        }
    });

    // Escape regex characters. Makes it easier for the chatbot to find the actual intents and patterns 
    function escapeRegex(str) {
        return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }

    /** Attempts to match the user's message with the patterns created
     * in the intents.json file
     */
    function findIntent(message) {
        const matches = [];

        for (let intent of intents) {
            for (let pattern of intent.patterns) {

                const escaped = escapeRegex(pattern.toLowerCase());
                const regex = new RegExp("\\b" + escaped + "\\b", "i");

                if (regex.test(message)) {
                    matches.push(intent);
                }
            }
        }

        if (matches.length === 1) return matches[0];

        // Signals a multi-intent situation when the intents are more than one
        if (matches.length > 1) {
            return { tag: "multi_intent" };
        }

        return null; // Return when no matches were found
    }


    /** Main logic for deciding how the chatbot responds */
    function processBotReply(userMessage) {

        // If intents are failed to load, gibe a nice feedback to the user
        if (!intents || intents.length === 0) {
            addBotMessage("I can't load my data right now");
            return;
        }

        const message = userMessage.toLowerCase();

        // Prevent multiple greetings
        if (
            hasGreeted &&
            (/\bhi\b|\bhello\b|\bhey\b/i.test(message))
        ) {
            return;
        }

        // Attempts to find the best intent
        let bestIntent = findIntent(message);

        // Tracks the number the chatbot has greeted 
        if (bestIntent.tag === "greeting") {
            hasGreeted = true;
        }

        // Picks a ranodm response form the matched intent
        const responses = bestIntent.responses;
        const reply = responses[Math.floor(Math.random() * responses.length)];

        addBotMessage(reply);
    }
});
