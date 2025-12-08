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
        // Clean message
        const cleanedMessage = message.toLowerCase().replace(/[^\w\s]/g, " ").trim();
        const msgWords = cleanedMessage.split(/\s+/);

        // Common filler words we ignore
        const stopWords = new Set(["what", "how", "the", "is", "are", "can", "should", "i", "for", "to", "of", "in"]);
        
        // Remove filler words from message
        const filteredMsgWords = msgWords.filter(w => !stopWords.has(w));

        let bestIntent = null;
        let bestScore = 0;

        // Loop through intents
        for (let intent of intents) {
            for (let pattern of intent.patterns) {
                
                const cleanedPattern = pattern.toLowerCase().replace(/[^\w\s]/g, " ").trim();
                const patternWords = cleanedPattern.split(/\s+/);

                // Remove filler words from patterns too
                const filteredPatternWords = patternWords.filter(w => !stopWords.has(w));

                // Count matches
                let score = 0;
                for (let pw of filteredPatternWords) {
                    if (filteredMsgWords.includes(pw)) {
                        score += 1;
                    }
                }

                // AUTOMATIC SYNONYMS (expandable)
                const synonyms = {
                    "lose": ["reduce", "drop", "burn"],
                    "weight": ["fat", "bodyfat"],
                    "foods": ["food", "meal", "meals"],
                    "exercise": ["workout", "training", "activity"]
                };

                filteredPatternWords.forEach(pw => {
                    if (synonyms[pw]) {
                        synonyms[pw].forEach(syn => {
                            if (filteredMsgWords.includes(syn)) score += 0.8;
                        });
                    }
                });

                // Normalize score by pattern length
                let finalScore = score / filteredPatternWords.length;

                if (finalScore > bestScore && finalScore >= 0.4) { 
                    bestScore = finalScore;
                    bestIntent = intent;
                }
            }
        }

        return bestIntent;
    }


    /** Main logic for deciding how the chatbot responds */
    function processBotReply(userMessage) {

        // Stop the bot if intents haven't loaded yet
        if (!intents || intents.length === 0) {
            addBotMessage("I'm still loading... try again in a moment!");
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

        // If no intent found
        if (!bestIntent) {
            addBotMessage("I'm not sure I understand. Could you rephrase that?");
            return;
        }

        // If multiple intents matched
        if (bestIntent.tag === "multi_intent") {
            addBotMessage("It seems like you're asking more than one thing. Try asking one question at a time!");
            return;
        }

        // Mark greeting
        if (bestIntent.tag === "greeting") {
            hasGreeted = true;
        }

        // Ensure responses exists
        if (!bestIntent.responses || bestIntent.responses.length === 0) {
            addBotMessage("I don't have an answer prepared for that yet!");
            return;
        }

        // Picks a random response from the matched intent
        const responses = bestIntent.responses;
        const reply = responses[Math.floor(Math.random() * responses.length)];

        addBotMessage(reply);
    }
});
