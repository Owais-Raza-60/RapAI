const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatBox = document.getElementById("chatBox");

function addMessage(text, type) {
    const message = document.createElement("div");
    message.classList.add("message");

    if (type === "user") {
        message.classList.add("user-message");
    } else {
        message.classList.add("ai-message");
    }

    message.textContent = text;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;

    return message;
}

function resizeInput() {
    input.style.height = "auto";
    input.style.height = `${Math.min(input.scrollHeight, 120)}px`;
}

function setLoadingState(isLoading) {
    sendButton.disabled = isLoading;
    sendButton.style.opacity = isLoading ? "0.7" : "1";
    sendButton.style.cursor = isLoading ? "wait" : "pointer";
}

function sendMessage() {
    const message = input.value.trim();

    if (message === "") {
        return;
    }

    addMessage(message, "user");
    input.value = "";
    resizeInput();

    const botReply = addMessage("RapAI is spittin’ the bars...", "ai");
    setLoadingState(true);

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
    })
        .then((response) => response.json())
        .then((data) => {
            botReply.textContent = data.reply || "Yo, the beat got me stuttering—try that again.";
        })
        .catch(() => {
            botReply.textContent = "Yo, the beat cut out—I’ll come back with the rhyme.";
        })
        .finally(() => {
            setLoadingState(false);
            input.focus();
        });
}

sendButton.addEventListener("click", sendMessage);

input.addEventListener("input", resizeInput);

input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});