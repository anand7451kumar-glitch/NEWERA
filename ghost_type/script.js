
const $ = (id) => document.getElementById(id);

const passages = [
  "Great developers are not born with perfect skills. They build their abilities through curiosity, consistent practice, and the courage to solve difficult problems one line at a time.",
  "The best way to learn programming is to build something useful. Start with a small idea, understand every line of code, and improve your project through experimentation.",
  "Technology moves quickly, but strong fundamentals remain valuable. Learn to think clearly, break problems into smaller pieces, and write code that other people can understand.",
  "Discipline beats motivation when motivation disappears. Every focused session is another opportunity to improve your skills and move closer to your goals.",
  "A computer follows instructions exactly. The challenge is learning to express your ideas clearly enough that a machine can transform them into something meaningful."
];

const STORAGE_KEY = "ghosttype-data-v1";

let duration = 30;
let timeLeft = duration;
let timer = null;
let started = false;
let finished = false;
let passage = "";
let bestWpm = 0;
let history = [];

function loadData() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");

    bestWpm = Number.isFinite(saved.bestWpm)
      ? Math.max(0, saved.bestWpm)
      : 0;

    history = Array.isArray(saved.history)
      ? saved.history.filter((item) =>
          item &&
          Number.isFinite(item.wpm) &&
          Number.isFinite(item.accuracy) &&
          Number.isFinite(item.characters) &&
          Number.isFinite(item.duration)
        ).slice(0, 20)
      : [];
  } catch {
    bestWpm = 0;
    history = [];
  }
}

function saveData() {
  try {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ bestWpm, history })
    );
  } catch {
    showToast("Unable to save. Check browser storage settings.");
  }
}

function choosePassage() {
  const previous = passage;
  const options = passages.filter((item) => item !== previous);

  passage = options[Math.floor(Math.random() * options.length)];
}

function getMetrics() {
  const input = $("typingInput").value;
  let correct = 0;
  let mistakes = 0;

  for (let i = 0; i < input.length; i++) {
    if (i < passage.length && input[i] === passage[i]) {
      correct++;
    } else {
      mistakes++;
    }
  }

  const elapsed = started
    ? Math.max(1, duration - timeLeft)
    : 0;

  const minutes = elapsed / 60;
  const wpm = minutes > 0
    ? Math.round((correct / 5) / minutes)
    : 0;

  const accuracy = input.length > 0
    ? Math.round((correct / input.length) * 100)
    : 100;

  return {
    input,
    correct,
    mistakes,
    characters: input.length,
    wpm,
    accuracy
  };
}

function renderPassage() {
  const input = $("typingInput").value;
  const display = $("textDisplay");

  display.replaceChildren();

  for (let i = 0; i < passage.length; i++) {
    const character = document.createElement("span");
    character.textContent = passage[i];

    if (i < input.length) {
      character.className = input[i] === passage[i]
        ? "correct"
        : "incorrect";
    } else if (i === input.length && !finished) {
      character.className = "current";
    }

    display.appendChild(character);
  }
}

function renderMetrics() {
  const metrics = getMetrics();

  $("wpm").textContent = metrics.wpm;
  $("accuracy").innerHTML =
    `${metrics.accuracy}<span class="unit">%</span>`;

  $("timeLeft").innerHTML =
    `${timeLeft}<span class="unit">s</span>`;

  $("bestWpm").textContent = bestWpm;
  $("characterCount").textContent =
    `${metrics.characters} characters typed`;

  $("totalCharacters").textContent = metrics.characters;
  $("correctCharacters").textContent = metrics.correct;
  $("mistakes").textContent = metrics.mistakes;

  const progress = ((duration - timeLeft) / duration) * 100;
  $("progressFill").style.width = `${progress}%`;
}

function setStatus(message) {
  $("testStatus").textContent = message;
}

function startTest() {
  if (started || finished) return;

  started = true;

  $("typingInput").disabled = false;
  $("startButton").textContent = "TEST IN PROGRESS...";
  $("typingInput").focus();

  setStatus("SESSION ACTIVE");
  showToast("Test initialized. Type accurately!");

  timer = setInterval(() => {
    timeLeft--;
    renderMetrics();

    if (timeLeft <= 0) {
      finishTest();
    }
  }, 1000);
}

function finishTest() {
  if (finished) return;

  finished = true;
  started = false;

  clearInterval(timer);
  timer = null;

  $("typingInput").disabled = true;
  $("startButton").classList.add("hidden");

  setStatus("SESSION COMPLETE");

  const metrics = getMetrics();

  const result = {
    wpm: metrics.wpm,
    accuracy: metrics.accuracy,
    characters: metrics.characters,
    duration,
    date: new Date().toISOString()
  };

  history.unshift(result);
  history = history.slice(0, 20);

  const newRecord = metrics.wpm > bestWpm;

  if (newRecord) {
    bestWpm = metrics.wpm;
  }

  saveData();
  renderMetrics();
  renderHistory();
  renderOperatorStats();

  $("finalWpm").textContent = metrics.wpm;
  $("finalAccuracy").textContent = `${metrics.accuracy}%`;
  $("finalCharacters").textContent = metrics.characters;

  $("resultGrade").textContent = getGrade(metrics.wpm);
  $("resultTitle").textContent = newRecord
    ? "New personal record!"
    : "Run complete.";

  $("resultMessage").textContent = newRecord
    ? "You just set your fastest score. Keep pushing your limits."
    : getFeedback(metrics.wpm, metrics.accuracy);

  $("resultPanel").classList.remove("hidden");

  showToast(newRecord ? "NEW PERSONAL RECORD!" : "Session saved.");
}

function getGrade(wpm) {
  if (wpm >= 100) return "S";
  if (wpm >= 80) return "A";
  if (wpm >= 60) return "B";
  if (wpm >= 40) return "C";
  return "D";
}

function getFeedback(wpm, accuracy) {
  if (accuracy < 85) {
    return "Slow down a little and focus on hitting the correct keys.";
  }

  if (wpm >= 80) {
    return "Excellent speed! Focus on maintaining that accuracy.";
  }

  if (wpm >= 50) {
    return "Solid performance. Keep practising to build consistency.";
  }

  return "Every session counts. Practise regularly and your speed will grow.";
}

function resetTest() {
  clearInterval(timer);
  timer = null;

  started = false;
  finished = false;
  timeLeft = duration;

  choosePassage();

  $("typingInput").value = "";
  $("typingInput").disabled = true;

  $("startButton").classList.remove("hidden");
  $("startButton").innerHTML = 'INITIALIZE TEST <span>→</span>';

  $("resultPanel").classList.add("hidden");

  setStatus("READY TO DEPLOY");

  renderPassage();
  renderMetrics();
}

function renderHistory() {
  const container = $("historyList");
  container.replaceChildren();

  if (history.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-history";
    empty.textContent =
      "No completed tests yet. Your first run awaits.";

    container.appendChild(empty);
    return;
  }

  for (const item of history) {
    const row = document.createElement("article");
    row.className = "history-item";

    const details = document.createElement("div");
    const speed = document.createElement("strong");
    speed.textContent = `${item.wpm} WPM`;

    const date = document.createElement("small");
    date.textContent = new Date(item.date).toLocaleString();

    details.append(speed, date);

    const accuracy = document.createElement("span");
    accuracy.className = "history-accuracy";
    accuracy.textContent = `${item.accuracy}%`;

    const time = document.createElement("span");
    time.className = "history-accuracy";
    time.textContent = `${item.duration}s`;

    row.append(details, accuracy, time);
    container.appendChild(row);
  }
}

function renderOperatorStats() {
  $("testsCompleted").textContent = history.length;

  const average = history.length
    ? Math.round(
        history.reduce((sum, item) => sum + item.wpm, 0) /
        history.length
      )
    : 0;

  const accuracy = history.length
    ? Math.max(...history.map((item) => item.accuracy))
    : 0;

  $("averageWpm").textContent = average;
  $("bestAccuracy").textContent = `${accuracy}%`;
}

let toastTimeout;

function showToast(message) {
  const toast = $("toast");

  toast.textContent = message;
  toast.classList.add("show");

  clearTimeout(toastTimeout);

  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 2400);
}

function handleTyping() {
  if (!started || finished) return;

  const input = $("typingInput").value;

  // Do not allow typing beyond the displayed passage.
  if (input.length > passage.length) {
    $("typingInput").value = input.slice(0, passage.length);
  }

  renderPassage();
  renderMetrics();

  if ($("typingInput").value.length >= passage.length) {
    finishTest();
  }
}

function initialize() {
  loadData();
  choosePassage();

  document.querySelectorAll(".mode-button").forEach((button) => {
    button.addEventListener("click", () => {
      if (started) {
        showToast("Finish or restart the current test first.");
        return;
      }

      duration = Number(button.dataset.time);
      timeLeft = duration;

      document.querySelectorAll(".mode-button").forEach((item) => {
        item.classList.toggle("active", item === button);
      });

      resetTest();
    });
  });

  $("startButton").addEventListener("click", startTest);
  $("typingInput").addEventListener("input", handleTyping);

  $("resetButton").addEventListener("click", resetTest);
  $("againButton").addEventListener("click", resetTest);

  $("clearHistoryButton").addEventListener("click", () => {
    if (history.length === 0) {
      showToast("No history to clear.");
      return;
    }

    const confirmed = window.confirm(
      "Clear all completed sessions and your saved personal record?"
    );

    if (!confirmed) return;

    history = [];
    bestWpm = 0;

    saveData();
    renderHistory();
    renderOperatorStats();
    renderMetrics();

    showToast("History cleared.");
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Tab" && event.shiftKey === false) {
      // Allow normal Tab navigation.
      return;
    }

    if (
      event.key === "Enter" &&
      event.metaKey &&
      !started
    ) {
      event.preventDefault();
      resetTest();
    }
  });

  renderPassage();
  renderMetrics();
  renderHistory();
  renderOperatorStats();
}

initialize();
