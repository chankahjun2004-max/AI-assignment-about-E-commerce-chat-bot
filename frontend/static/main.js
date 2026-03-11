document.addEventListener("DOMContentLoaded", function () {
    const msgerForm = document.querySelector(".msger-inputarea");
    const msgerInput = document.querySelector(".msger-input");
    const modelCards = document.querySelectorAll(".model-card");
    const chatTitle = document.getElementById("chat-title");

    // Chat history storage (one per model)
    const chatHistories = {
        "1": [],
        "2": [],
        "3": []
    };

    // Default model
    let currentModel = "1";
    updateChatBox(currentModel);

    // Listen for model selection (switch between chat boxes)
    modelCards.forEach(card => {
        card.addEventListener("click", () => {
            currentModel = card.dataset.model;
            chatTitle.textContent = card.querySelector("h4").textContent;

            updateModelHighlight(currentModel);
            updateChatBox(currentModel);
        });
    });

    // Message submission logic
    msgerForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const msgText = msgerInput.value.trim();
        if (!msgText) return;

        const userMsg = createMessageHTML("You", "right-msg", msgText);
        chatHistories[currentModel].push(userMsg);
        appendMessageHTML(currentModel, userMsg);

        msgerInput.value = "";

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msgText, model: currentModel }),
            });

            const data = await response.json();
            if (data.response) {
                const botMsg = createMessageHTML("BOT", "left-msg", data.response);
                chatHistories[currentModel].push(botMsg);
                appendMessageHTML(currentModel, botMsg);
            }
        } catch (error) {
            console.error("Error fetching chatbot response:", error);
        }
    });

    // Functions
    function createMessageHTML(name, side, text) {
        return `
            <div class="msg ${side}">
                <div class="msg-bubble">
                    <div class="msg-info">
                        <div class="msg-info-name">${name}</div>
                    </div>
                    <div class="msg-text">${text}</div>
                </div>
            </div>
        `;
    }

    function appendMessageHTML(model, msgHTML) {
        const chatBox = document.querySelector(`#chat-${getModelName(model)}`);
        chatBox.insertAdjacentHTML("beforeend", msgHTML);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function updateChatBox(selectedModel) {
        document.querySelectorAll(".msger-chat").forEach(chat => {
            chat.classList.add("hidden");
        });

        const activeChatBox = document.querySelector(`#chat-${getModelName(selectedModel)}`);
        if (activeChatBox) activeChatBox.classList.remove("hidden");

        loadChatHistory(selectedModel);
    }

    function loadChatHistory(model) {
        const chatBox = document.querySelector(`#chat-${getModelName(model)}`);
        if (!chatBox) return;

        chatBox.innerHTML = ""; // Clear the chat
        chatHistories[model].forEach(html => appendMessageHTML(model, html));
    }

    function updateModelHighlight(selectedModel) {
        modelCards.forEach(card => {
            card.classList.toggle("selected", card.dataset.model === selectedModel);
        });
    }

    function getModelName(model) {
        return model === "1" ? "gemma" : model === "2" ? "llama" : "mistral";
    }
});
