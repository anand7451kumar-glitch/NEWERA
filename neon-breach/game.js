
// ============================================
// NEON//BREACH
// MISSION 01: THE FIRST FIREWALL
// ============================================

const MAX_ATTEMPTS = 10;
const STORAGE_KEY = "neon-breach-best-v1";

// Game state
let secretCode = "";
let attempts = 0;
let gameOver = false;
let history = [];
let startTime = 0;

// DOM helper
const $ = (id) => document.getElementById(id);

// ============================================
// 1. GENERATE SECRET CODE
// ============================================

function generateSecretCode() {
  const digits = [];

  while (digits.length < 4) {
    const digit = Math.floor(Math.random() * 10).toString();

    if (!digits.includes(digit)) {
      digits.push(digit);
    }
  }

  return digits.join("");
}

// ============================================
// 2. UPDATE TERMINAL CLOCK
// ============================================

function updateClock() {
  const now = new Date();

  $("clock").textContent = now.toLocaleTimeString("en-GB", {
    hour12: false
  });
}

// ============================================
// 3. TERMINAL MESSAGES
// ============================================

function addTerminalMessage(message, type = "") {
  const terminal = $("terminalMessage");
  const paragraph = document.createElement("p");

  if (type === "green") {
    paragraph.className = "terminal-green";
  } else if (type === "warning") {
    paragraph.className = "terminal-warning";
  } else if (type === "ready") {
    paragraph.className = "terminal-ready";
  }

  paragraph.textContent = message;
  terminal.appendChild(paragraph);

  // Keep the terminal log manageable
  while (terminal.children.length > 12) {
    terminal.removeChild(terminal.firstElementChild);
  }
}

// ============================================
// 4. SECURITY TRACE
// ============================================

function updateTrace() {
  const trace = Math.round((attempts / MAX_ATTEMPTS) * 100);

  $("traceNumber").innerHTML = `${trace}<span>%</span>`;
  $("traceFill").style.width = `${trace}%`;

  $("attemptNumber").textContent = MAX_ATTEMPTS - attempts;

  const dots = $("attemptDots").children;

  Array.from(dots).forEach((dot, index) => {
    dot.classList.toggle("used", index < attempts);
  });

  if (trace >= 70) {
    $("traceFill").classList.add("danger");
    $("traceCaption").classList.add("danger");
    $("traceCaption").textContent = "CRITICAL DETECTION";
  } else if (trace >= 40) {
    $("traceFill").classList.remove("danger");
    $("traceCaption").classList.remove("danger");
    $("traceCaption").textContent = "TRACE DETECTED";
  } else {
    $("traceFill").classList.remove("danger");
    $("traceCaption").classList.remove("danger");
    $("traceCaption").textContent = "UNDETECTED";
  }
}

// ============================================
// 5. UPDATE CODE DISPLAY
// ============================================

function updateCodeDisplay(value = "") {
  const slots = $("codeDisplay").children;

  for (let i = 0; i < 4; i++) {
    slots[i].textContent = value[i] || "?";
  }
}

// ============================================
// 6. VALIDATE INPUT
// ============================================

function validateGuess(guess) {
  if (!/^\d{4}$/.test(guess)) {
    return "ENTER EXACTLY FOUR DIGITS.";
  }

  if (new Set(guess).size !== 4) {
    return "REPEATED DIGITS DETECTED. USE FOUR UNIQUE DIGITS.";
  }

  return null;
}

// ============================================
// 7. CHECK THE GUESS
// ============================================

function calculateFeedback(guess) {
  let correctPosition = 0;
  let correctDigit = 0;

  for (let i = 0; i < 4; i++) {
    if (guess[i] === secretCode[i]) {
      correctPosition++;
    } else if (secretCode.includes(guess[i])) {
      correctDigit++;
    }
  }

  return { correctPosition, correctDigit };
}

// ============================================
// 8. ADD ATTEMPT TO DECRYPTION LOG
// ============================================

function addHistory(guess, feedback) {
  history.push({
    guess,
    correctPosition: feedback.correctPosition,
    correctDigit: feedback.correctDigit
  });

  $("historyCount").textContent =
    `${history.length} ${history.length === 1 ? "ENTRY" : "ENTRIES"}`;

  const list = $("historyList");

  if (history.length === 1) {
    list.innerHTML = "";
  }

  const row = document.createElement("div");
  row.className = "history-row";

  const attemptLabel = document.createElement("span");
  attemptLabel.className = "history-attempt";
  attemptLabel.textContent = `#${history.length}`;

  const guessLabel = document.createElement("span");
  guessLabel.className = "history-guess";
  guessLabel.textContent = guess;

  const feedbackLabel = document.createElement("span");
  feedbackLabel.className = "history-feedback";

  const green = document.createElement("span");
  green.textContent = `${feedback.correctPosition} GREEN`;

  const yellow = document.createElement("span");
  yellow.className = "yellow";
  yellow.textContent = ` ${feedback.correctDigit} YELLOW`;

  feedbackLabel.append(green, yellow);
  row.append(attemptLabel, guessLabel, feedbackLabel);

  list.prepend(row);
}

// ============================================
// 9. HANDLE A GUESS
// ============================================

function submitGuess() {
  if (gameOver) return;

  const input = $("codeInput");
  const guess = input.value.trim();

  const error = validateGuess(guess);

  if (error) {
    $("gameMessage").textContent = `[ ERROR ] ${error}`;
    addTerminalMessage(`[ INPUT ERROR ] ${error}`, "warning");
    input.focus();
    return;
  }

  attempts++;

  const feedback = calculateFeedback(guess);

  updateTrace();
  updateCodeDisplay(guess);
  addHistory(guess, feedback);

  addTerminalMessage(
    `[ ATTEMPT ${attempts} ] CODE TRANSMITTED: ${guess}`
  );

  addTerminalMessage(
    `[ ANALYSIS ] ${feedback.correctPosition} POSITION MATCHES / ${feedback.correctDigit} DIGIT MATCHES`
  );

  if (guess === secretCode) {
    $("gameMessage").textContent = "[ SUCCESS ] ACCESS KEY VERIFIED.";
    addTerminalMessage("[ SYSTEM ] FIREWALL DEFEATED.", "green");

    endGame(true);
    return;
  }

  if (attempts >= MAX_ATTEMPTS) {
    $("gameMessage").textContent = "[ FAILURE ] SECURITY LOCKDOWN.";
    addTerminalMessage("[ SYSTEM ] TRACE COMPLETE. ACCESS DENIED.", "warning");

    endGame(false);
    return;
  }

  const remaining = MAX_ATTEMPTS - attempts;

  $("gameMessage").textContent =
    `[ ANALYSIS ] ${feedback.correctPosition} GREEN / ${feedback.correctDigit} YELLOW — ${remaining} ATTEMPTS LEFT`;

  input.value = "";
  input.focus();
}

// ============================================
// 10. SAVE BEST RESULT
// ============================================

function saveBestResult() {
  const previous = JSON.parse(
    localStorage.getItem(STORAGE_KEY) || "null"
  );

  const current = {
    attempts,
    time: Math.floor((Date.now() - startTime) / 1000),
    date: new Date().toISOString()
  };

  // Fewer attempts is a better result
  if (!previous || current.attempts < previous.attempts) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(current));
    return true;
  }

  return false;
}

// ============================================
// 11. END GAME
// ============================================

function endGame(won) {
  gameOver = true;

  $("codeInput").disabled = true;
  $("submitButton").disabled = true;

  $("resultOverlay").classList.remove("hidden");

  const card = document.querySelector(".result-card");

  card.classList.toggle("failure", !won);

  $("resultIcon").textContent = won ? "✓" : "×";
  $("resultLabel").textContent = won
    ? "ACCESS GRANTED"
    : "ACCESS DENIED";

  $("resultTitle").textContent = won
    ? "FIREWALL BREACHED"
    : "SECURITY LOCKDOWN";

  $("resultDescription").textContent = won
    ? `You cracked the gateway in ${attempts} attempt${attempts === 1 ? "" : "s"}. The network is yours.`
    : "The security system detected your activity. The gateway is locked.";

  $("resultCode").textContent = secretCode;

  if (won) {
    const isNewBest = saveBestResult();

    if (isNewBest) {
      $("resultDescription").textContent += " NEW PERSONAL BEST!";
    }
  }

  $("connectionStatus").textContent = won
    ? "GATEWAY COMPROMISED"
    : "CONNECTION TERMINATED";
}

// ============================================
// 12. RESTART GAME
// ============================================

function restartGame() {
  secretCode = generateSecretCode();
  attempts = 0;
  gameOver = false;
  history = [];
  startTime = Date.now();

  $("codeInput").value = "";
  $("codeInput").disabled = false;

  $("submitButton").disabled = false;

  $("resultOverlay").classList.add("hidden");

  $("result-card")?.classList.remove("failure");

  document.querySelector(".result-card").classList.remove("failure");

  $("traceNumber").innerHTML = '00<span>%</span>';
  $("traceFill").style.width = "0%";
  $("traceFill").classList.remove("danger");

  $("traceCaption").textContent = "UNDETECTED";
  $("traceCaption").classList.remove("danger");

  $("attemptNumber").textContent = MAX_ATTEMPTS;

  Array.from($("attemptDots").children).forEach((dot) => {
    dot.classList.remove("used");
  });

  updateCodeDisplay();

  $("gameMessage").textContent = "AWAITING YOUR FIRST ATTEMPT...";

  $("historyCount").textContent = "0 ENTRIES";
  $("historyList").innerHTML = `
    <div class="history-empty">
      NO DATA RECORDED. BEGIN THE BREACH.
    </div>
  `;

  $("terminalMessage").innerHTML = `
    <p class="terminal-green">[ SYSTEM ] NEW BREACH SESSION INITIALIZED.</p>
    <p>[ SYSTEM ] ENCRYPTED GATEWAY DETECTED.</p>
    <p>[ SYSTEM ] ACCESS KEY REQUIRED.</p>
    <p class="terminal-warning">[ WARNING ] UNAUTHORIZED ACCESS IS TRACEABLE.</p>
    <p class="terminal-ready">[ READY ] AWAITING INPUT_</p>
  `;

  $("connectionStatus").textContent = "SECURE CONNECTION";

  addTerminalMessage("[ SYSTEM ] NEW SESSION READY.", "green");

  $("codeInput").focus();
}

// ============================================
// 13. EVENT LISTENERS
// ============================================

function setupEvents() {
  $("submitButton").addEventListener("click", submitGuess);

  $("codeInput").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      submitGuess();
    }
  });

  $("codeInput").addEventListener("input", (event) => {
    const clean = event.target.value.replace(/\D/g, "").slice(0, 4);
    event.target.value = clean;
    updateCodeDisplay(clean);
  });

  $("restartButton").addEventListener("click", restartGame);
}

// ============================================
// 14. INITIALIZE GAME
// ============================================

function initGame() {
  secretCode = generateSecretCode();
  startTime = Date.now();

  setupEvents();
  updateClock();

  // Refresh clock every second
  setInterval(updateClock, 1000);

  $("codeInput").focus();

  console.log("NEON//BREACH initialized.");
}

// Start after page loads
document.addEventListener("DOMContentLoaded", initGame);
