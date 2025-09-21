// ---------------------------
// DOM ELEMENTS
// ---------------------------
const chatBox = document.getElementById("chat");       // The container for chat messages
const chatInput = document.getElementById("chatInput"); // The input field where user types
const micBtn = document.getElementById("micBtn");      // Button to send text or start voice

// ---------------------------
// SPEECH RECOGNITION SETUP
// ---------------------------
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.continuous = false; // Only listen once per activation
recognition.lang = "en-US";     // Language for recognition

// ---------------------------
// CHANGE BUTTON ICON BASED ON INPUT
// ---------------------------
chatInput.addEventListener("input", () => {
  if (chatInput.value.trim() !== "") {
    micBtn.innerHTML = "➤"; // Show send icon when text is typed
    micBtn.title = "Send";
  } else {
    micBtn.innerHTML = "🎤"; // Show mic icon when input is empty
    micBtn.title = "Use voice mode";
  }
});

// ---------------------------
// HANDLE ENTER KEY
// ---------------------------
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && chatInput.value.trim() !== "") {
    e.preventDefault();    // Prevent newline in input
    micBtn.click();        // Trigger the button click logic
  }
});

// ---------------------------
// HANDLE BUTTON CLICK (SEND OR MIC)
// ---------------------------
micBtn.addEventListener("click", () => {
  if (chatInput.value.trim() !== "") {
    // 1️⃣ User typed text
    const text = chatInput.value.trim();

    addMessage(text, "user-message"); // Show user message
    chatInput.value = "";             // Clear input
    micBtn.innerHTML = "🎤";          // Reset icon to mic
    micBtn.title = "Use voice mode";

    mockBotReply(text);               // Call bot reply function
  } else {
    // 2️⃣ No text, start voice recognition
    recognition.start();
  }
});

// ---------------------------
// SPEECH RECOGNITION RESULT
// ---------------------------
recognition.onresult = (event) => {
  const transcript = event.results[0][0].transcript;  // Get recognized speech text

  addMessage(transcript, "user-message"); // Show as user message
  chatInput.value = transcript;           // Optionally show in input

  mockBotReply(transcript);               // Call bot reply function
};

// ---------------------------
// FUNCTION TO ADD MESSAGES TO CHAT BOX
// ---------------------------
function addMessage(text, className) {
  const msg = document.createElement("div");
  msg.classList.add("message", className); // Add proper styling class
  msg.textContent = text;                  // Set message text
  chatBox.appendChild(msg);                // Add to chat container
  chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}

// ---------------------------
// FUNCTION TO HANDLE BOT REPLY
// ---------------------------
function mockBotReply(userText) {
  // Using setTimeout to simulate delay
  setTimeout(() => {
    addMessage("Bot reply: " + userText, "bot-message");
  }, 1000);
}
// In real implementation, replace mockBotReply with actual API call to get bot response


