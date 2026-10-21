
const $ = (id) => document.getElementById(id);

const moves = {
  rock: { emoji: "✊", name: "Rock" },
  paper: { emoji: "✋", name: "Paper" },
  scissors: { emoji: "✌️", name: "Scissors" }
};

let playerScore = 0;
let computerScore = 0;
let currentStreak = 0;
let bestStreak = 0;
let round = 0;
let history = [];

const buttons = document.querySelectorAll(".choice-button");

function getComputerChoice() {
  const choices = Object.keys(moves);
  return choices[Math.floor(Math.random() * choices.length)];
}

function getOutcome(player, computer) {
  if (player === computer) return "draw";

  const playerWins =
    (player === "rock" && computer === "scissors") ||
    (player === "paper" && computer === "rock") ||
    (player === "scissors" && computer === "paper");

  return playerWins ? "win" : "lose";
}

function updateScoreboard() {
  $("playerScore").textContent = playerScore;
  $("computerScore").textContent = computerScore;
  $("currentStreak").textContent = currentStreak;
  $("bestStreak").textContent = bestStreak;
  $("roundNumber").textContent = String(round + 1).padStart(2, "0");
}

function showResult(outcome, player, computer) {
  const resultBox = $("resultBox");

  resultBox.className = "result-box";

  if (outcome === "win") {
    resultBox.classList.add("win");
    $("resultTitle").textContent = "✦ You win this round!";
    $("resultMessage").textContent =
      `${moves[player].name} beats ${moves[computer].name}. Nice move!`;
  } else if (outcome === "lose") {
    resultBox.classList.add("lose");
    $("resultTitle").textContent = "The computer wins!";
    $("resultMessage").textContent =
      `${moves[computer].name} beats ${moves[player].name}. Try again!`;
  } else {
    resultBox.classList.add("draw");
    $("resultTitle").textContent = "It's a draw!";
    $("resultMessage").textContent =
      `Both chose ${moves[player].name}. Great minds think alike.`;
  }
}

function renderHistory() {
  const list = $("historyList");
  list.replaceChildren();

  $("historyCount").textContent = `${history.length} ROUND${history.length === 1 ? "" : "S"}`;

  if (history.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-history";
    empty.textContent = "Your battles will appear here.";
    list.append(empty);
    return;
  }

  for (const item of history.slice(0, 5)) {
    const row = document.createElement("div");
    row.className = "history-item";

    const left = document.createElement("div");
    left.className = "history-left";

    const number = document.createElement("span");
    number.style.color = "#8e8ba8";
    number.textContent = `#${String(item.round).padStart(2, "0")}`;

    const description = document.createElement("span");
    description.textContent =
      `${moves[item.player].emoji} ${moves[item.player].name} vs ${moves[item.computer].name} ${moves[item.computer].emoji}`;

    const outcome = document.createElement("span");
    outcome.className = `history-outcome ${item.outcome}`;
    outcome.textContent =
      item.outcome === "win" ? "WIN" :
      item.outcome === "lose" ? "LOSS" : "DRAW";

    left.append(number, description);
    row.append(left, outcome);
    list.append(row);
  }
}

function play(player) {
  if (!moves[player]) return;

  const computer = getComputerChoice();
  const outcome = getOutcome(player, computer);

  round++;

  $("playerHand").textContent = moves[player].emoji;
  $("computerHand").textContent = moves[computer].emoji;
  $("playerChoice").textContent = moves[player].name;
  $("computerChoice").textContent = moves[computer].name;

  // Restart the animation on every round.
  for (const id of ["playerHand", "computerHand"]) {
    const hand = $(id);
    hand.classList.remove("shake");
    void hand.offsetWidth;
    hand.classList.add("shake");
  }

  if (outcome === "win") {
    playerScore++;
    currentStreak++;
    bestStreak = Math.max(bestStreak, currentStreak);
  } else if (outcome === "lose") {
    computerScore++;
    currentStreak = 0;
  } else {
    currentStreak = 0;
  }

  history.unshift({ round, player, computer, outcome });

  updateScoreboard();
  showResult(outcome, player, computer);
  renderHistory();

  buttons.forEach(button => {
    button.classList.toggle("chosen", button.dataset.choice === player);
  });
}

buttons.forEach(button => {
  button.addEventListener("click", () => play(button.dataset.choice));
});

// Keyboard shortcuts: R = rock, P = paper, S = scissors.
document.addEventListener("keydown", event => {
  if (event.repeat || event.metaKey || event.ctrlKey || event.altKey) return;

  const tag = document.activeElement?.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;

  const keyMoves = { r: "rock", p: "paper", s: "scissors" };
  const choice = keyMoves[event.key.toLowerCase()];

  if (choice) play(choice);
});

$("resetButton").addEventListener("click", () => {
  playerScore = 0;
  computerScore = 0;
  currentStreak = 0;
  bestStreak = 0;
  round = 0;
  history = [];

  $("playerHand").textContent = "✊";
  $("computerHand").textContent = "✊";
  $("playerChoice").textContent = "Waiting...";
  $("computerChoice").textContent = "Ready...";
  $("resultBox").className = "result-box";
  $("resultTitle").textContent = "Ready to battle?";
  $("resultMessage").textContent = "Pick a move below to start your first round.";

  buttons.forEach(button => button.classList.remove("chosen"));

  updateScoreboard();
  renderHistory();
});

updateScoreboard();
renderHistory();
