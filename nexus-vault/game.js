const stages = [
  {
    icon: "⌘",
    type: "ACCESS CONTROL",
    title: "The First Lock",
    description: "An old terminal asks for its original administrator code.",
    clue: "RECOVERED NOTE:\n\"The circle never ends.\nStart with 3, then 1, then 4...\"",
    answer: "3141",
    placeholder: "ENTER 4 DIGITS",
    evidence: ["ADMIN CODE", "3141 — Original terminal access code recovered."]
  },
  {
    icon: "◈",
    type: "ENCRYPTED ARCHIVE",
    title: "The Hidden Word",
    description: "A corrupted archive contains a password hidden in plain sight.",
    clue: "RECOVERED MESSAGE:\n\"I am the path of every planet.\nI surround the sun, but never touch it.\nWhat am I?\"",
    answer: "orbit",
    placeholder: "ENTER THE WORD",
    evidence: ["ARCHIVE PASSWORD", "ORBIT — Archive password decoded."]
  },
  {
    icon: "△",
    type: "RESEARCH DATABASE",
    title: "The Missing Number",
    description: "A researcher left a numerical sequence in the database.",
    clue: "SEQUENCE:\n3, 6, 12, 24, ?\n\n\"Every number doubles. Find the next.\"",
    answer: "48",
    placeholder: "ENTER NUMBER",
    evidence: ["RESEARCH SEQUENCE", "48 — The next number in the sequence."]
  },
  {
    icon: "▣",
    type: "FINAL SECURITY",
    title: "The Last Door",
    description: "The vault's final lock needs a four-digit override assembled from your evidence.",
    clue: "FINAL TRANSMISSION:\n\"Take the first two digits of the admin code.\nThen take the last two digits of the research answer.\"\n\nADMIN CODE: 3141\nRESEARCH ANSWER: 48",
    answer: "3148",
    placeholder: "ENTER OVERRIDE",
    evidence: ["FINAL OVERRIDE", "3148 — The vault's master access sequence."]
  }
];

let currentStage = 0;
let completed = [];
let startTime = 0;
let elapsedSeconds = 0;
let timerInterval = null;

const beginBtn = document.getElementById("beginBtn");
const intro = document.querySelector(".intro");
const game = document.getElementById("game");
const restartBtn = document.getElementById("restartBtn");

const stageLabel = document.getElementById("stageLabel");
const puzzleIcon = document.getElementById("puzzleIcon");
const puzzleType = document.getElementById("puzzleType");
const puzzleTitle = document.getElementById("puzzleTitle");
const puzzleDescription = document.getElementById("puzzleDescription");
const clue = document.getElementById("clue");
const puzzleContent = document.getElementById("puzzleContent");
const feedback = document.getElementById("feedback");

const progress = document.getElementById("progress");
const progressBar = document.getElementById("progressBar");
const inventory = document.getElementById("inventory");
const operatorStatus = document.getElementById("operatorStatus");

function startGame() {
  currentStage = 0;
  completed = [];
  elapsedSeconds = 0;
  startTime = Date.now();

  clearInterval(timerInterval);

  intro.classList.add("hidden");
  game.classList.remove("hidden");

  operatorStatus.textContent = "IN PROGRESS";
  operatorStatus.style.color = "#64e6d1";

  renderStage();
  updateProgress();

  timerInterval = setInterval(() => {
    elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
  }, 1000);
}

function renderStage() {
  const stage = stages[currentStage];

  stageLabel.textContent =
    `SYSTEM 0${currentStage + 1} / ${stage.type}`;

  puzzleIcon.textContent = stage.icon;
  puzzleType.textContent = stage.type;
  puzzleTitle.textContent = stage.title;
  puzzleDescription.textContent = stage.description;
  clue.textContent = stage.clue;

  feedback.textContent = "";
  feedback.className = "feedback";

  puzzleContent.innerHTML = `
    <input
      id="answerInput"
      type="text"
      placeholder="${stage.placeholder}"
      autocomplete="off"
      maxlength="20"
      aria-label="Puzzle answer"
    >
    <button id="submitAnswer">UNLOCK ↗</button>
  `;

  const input = document.getElementById("answerInput");
  const submit = document.getElementById("submitAnswer");

  submit.addEventListener("click", checkAnswer);

  input.addEventListener("keydown", event => {
    if (event.key === "Enter") checkAnswer();
  });

  input.focus();
  renderInventory();
}

function checkAnswer() {
  const stage = stages[currentStage];
  const input = document.getElementById("answerInput");
  const answer = input.value.trim().toLowerCase();

  if (!answer) {
    showFeedback("Enter an answer first.");
    return;
  }

  if (answer !== stage.answer.toLowerCase()) {
    showFeedback("ACCESS DENIED. That answer is incorrect.");
    input.value = "";
    input.focus();
    return;
  }

  completed.push(stage.evidence);
  showFeedback("ACCESS GRANTED. Evidence recovered.", true);
  updateProgress();
  renderInventory();

  puzzleContent.innerHTML = `
    <button id="continueBtn">
      ${currentStage === stages.length - 1 ? "OPEN FINAL EXIT ↗" : "CONTINUE ↗"}
    </button>
  `;

  document.getElementById("continueBtn").addEventListener("click", () => {
    if (currentStage === stages.length - 1) {
      finishGame();
    } else {
      currentStage++;
      renderStage();
    }
  });
}

function showFeedback(message, success = false) {
  feedback.textContent = message;
  feedback.className = success ? "feedback success" : "feedback";
}

function updateProgress() {
  const count = completed.length;
  progress.textContent = `${count} / ${stages.length}`;
  progressBar.style.width = `${(count / stages.length) * 100}%`;
}

function renderInventory() {
  if (completed.length === 0) {
    inventory.innerHTML =
      '<div class="empty-inventory">No evidence recovered.</div>';
    return;
  }

  inventory.innerHTML = completed.map(item => `
    <div class="evidence">
      <strong>✓ ${item[0]}</strong>
      <span>${item[1]}</span>
    </div>
  `).join("");
}

function finishGame() {
  clearInterval(timerInterval);

  const previousBest = Number(localStorage.getItem("nexusBest")) || 0;
  const finalTime = Math.floor((Date.now() - startTime) / 1000);

  if (previousBest === 0 || finalTime < previousBest) {
    localStorage.setItem("nexusBest", finalTime);
  }

  operatorStatus.textContent = "ESCAPED";
  operatorStatus.style.color = "#64e6d1";

  stageLabel.textContent = "MISSION COMPLETE / EXIT OPEN";
  puzzleIcon.textContent = "✓";
  puzzleType.textContent = "SECURITY OVERRIDDEN";
  puzzleTitle.textContent = "YOU ARE FREE.";
  puzzleDescription.textContent =
    "The vault doors have opened. You successfully recovered every piece of evidence.";

  clue.textContent =
    `ALL FOUR SECURITY LAYERS DISABLED.\n\n` +
    `COMPLETION TIME: ${formatTime(finalTime)}\n` +
    `EVIDENCE RECOVERED: 4 / 4\n` +
    `FINAL OVERRIDE: 3148`;

  puzzleContent.innerHTML = `
    <button id="playAgain">PLAY AGAIN ↗</button>
  `;

  feedback.textContent = "MISSION SUCCESSFUL.";
  feedback.className = "feedback success";

  document.getElementById("playAgain").addEventListener("click", startGame);
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remaining = seconds % 60;

  return `${String(minutes).padStart(2, "0")}:${String(remaining).padStart(2, "0")}`;
}

function restartGame() {
  clearInterval(timerInterval);
  startGame();
}

beginBtn.addEventListener("click", startGame);
restartBtn.addEventListener("click", restartGame);