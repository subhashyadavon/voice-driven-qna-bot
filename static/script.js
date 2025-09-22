// ---------------------------
// DOM ELEMENTS
// ---------------------------
const chatBox = document.getElementById("chat");
const chatInput = document.getElementById("chatInput");
const micBtn = document.getElementById("micBtn");

// ---------------------------
// VOICE MODE OVERLAY
// ---------------------------
const voiceOverlay = document.createElement("div");
voiceOverlay.id = "voiceOverlay";
voiceOverlay.style.position = "fixed";
voiceOverlay.style.top = 0;
voiceOverlay.style.left = 0;
voiceOverlay.style.width = "100%";
voiceOverlay.style.height = "100%";
voiceOverlay.style.background = "rgba(0,0,0,0.85)";
voiceOverlay.style.display = "flex";
voiceOverlay.style.flexDirection = "column";
voiceOverlay.style.alignItems = "center";
voiceOverlay.style.justifyContent = "center";
voiceOverlay.style.color = "white";
voiceOverlay.style.fontSize = "24px";
voiceOverlay.style.zIndex = 9999;
voiceOverlay.style.display = "none"; // initially hidden

voiceOverlay.innerHTML = `
  <p id="listeningText">🎤 Listening...</p>
  <button id="stopVoiceBtn" style="
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 18px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  ">Stop</button>
`;

document.body.appendChild(voiceOverlay);

// ---------------------------
// UPLOAD FORM HANDLER
// ---------------------------
const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");

uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(uploadForm);

  if (!fileInput.files.length && !formData.get("url")) {
    alert("Please select a file or enter a URL.");
    return;
  }

  try {
    const response = await fetch("/upload", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    alert(data.message);

    // Clear input fields after successful upload
    fileInput.value = "";
    uploadForm.querySelector('input[name="url"]').value = "";

  } catch (err) {
    console.error(err);
    alert("Upload failed.");
  }
});

// ---------------------------
// SPEECH RECOGNITION SETUP
// ---------------------------
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.continuous = true;
recognition.interimResults = false;
recognition.lang = "en-US";

// ---------------------------
// CHANGE BUTTON ICON BASED ON INPUT
// ---------------------------
chatInput.addEventListener("input", () => {
  if (chatInput.value.trim() !== "") {
    micBtn.innerHTML = "➤";
    micBtn.title = "Send";
  } else {
    micBtn.innerHTML = "🎤";
    micBtn.title = "Use voice mode";
  }
});

// ---------------------------
// HANDLE ENTER KEY
// ---------------------------
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && chatInput.value.trim() !== "") {
    e.preventDefault();
    micBtn.click();
  }
});

// ---------------------------
// HANDLE BUTTON CLICK
// ---------------------------
micBtn.addEventListener("click", () => {
  if (chatInput.value.trim() !== "") {
    // Typed text
    const text = chatInput.value.trim();
    chatInput.value = "";
    micBtn.innerHTML = "🎤";
    micBtn.title = "Use voice mode";

    sendQueryToBot(text); // send typed text to backend
  } else {
    // Voice mode
    voiceOverlay.style.display = "flex";
    recognition.start();
  }
});

// ---------------------------
// SPEECH RECOGNITION RESULT
// ---------------------------
recognition.onresult = (event) => {
  const transcript = event.results[event.results.length - 1][0].transcript;
  chatInput.value = "";

  sendQueryToBot(transcript); // send voice transcript to backend
};

// ---------------------------
// STOP VOICE MODE
// ---------------------------
document.getElementById("stopVoiceBtn").addEventListener("click", () => {
  recognition.stop();
  voiceOverlay.style.display = "none";
});

// ---------------------------
// FUNCTION TO ADD MESSAGES TO CHAT
// ---------------------------
function addMessage(text, className) {
  const msg = document.createElement("div");
  msg.classList.add("message", className);
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ---------------------------
// SEND QUERY TO BOT
// ---------------------------
async function sendQueryToBot(userText) {
  // Display user message
  addMessage(userText, "user-message");

  try {
    const response = await fetch("/query", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({text: userText})
    });

    const data = await response.json();
    addMessage(data.answer, "bot-message"); // display bot reply
  } catch (err) {
    console.error(err);
    addMessage("Error fetching response from server", "bot-message");
  }
}





