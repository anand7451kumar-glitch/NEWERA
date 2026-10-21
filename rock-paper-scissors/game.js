
const $ = (id) => document.getElementById(id);

const moves = {
  rock: { emoji: "✊", name: "Rock" },
  paper: { emoji: "✋", name: "Paper" },
  scissors: { emoji: "✌️", name: "Scissors" }
};

const STORAGE_KEY = "rpsArenaSave";

const buttons = document.querySelectorAll(".choice-button");


const MATCH_TARGET = 3;

let matchPlayerScore = 0;
let matchComputerScore = 0;
let matchFinished = false;

function updateTournament() {
  $("matchPlayerScore").textContent = matchPlayerScore;
  $("matchComputerScore").textContent = matchComputerScore;

  const dots = $("matchProgress").querySelectorAll(".match-dot");

  dots.forEach((dot, index) => {
    dot.classList.remove("player-point", "computer-point");

    if (index < matchPlayerScore) {
      dot.classList.add("player-point");
    } else if (index < matchPlayerScore + matchComputerScore) {
      dot.classList.add("computer-point");
    }
  });

  const status = $("matchStatus");
  status.className = "tournament-badge";

  if (matchPlayerScore >= MATCH_TARGET) {
    status.textContent = "CHAMPION";
    status.classList.add("champion");
    $("matchMessage").textContent =
      "🏆 You are the champion! Restart the match to play again.";
  } else if (matchComputerScore >= MATCH_TARGET) {
    status.textContent = "MATCH LOST";
    status.classList.add("defeated");
    $("matchMessage").textContent =
      "The computer won this match. Restart and try again!";
  } else {
    status.textContent = "IN PROGRESS";
    const needed = MATCH_TARGET - matchPlayerScore;
    const computerNeeded = MATCH_TARGET - matchComputerScore;

    $("matchMessage").textContent =
      `First to 3 wins. You need ${needed}; computer needs ${computerNeeded}.`;
  }

  buttons.forEach(button => {
    button.disabled = matchFinished;
  });
}

function restartMatch() {
  matchPlayerScore = 0;
  matchComputerScore = 0;
  matchFinished = false;

  $("playerHand").textContent = "✊";
  $("computerHand").textContent = "✊";
  $("playerChoice").textContent = "Waiting...";
  $("computerChoice").textContent = "Ready...";
  $("resultBox").className = "result-box";
  $("resultTitle").textContent = "Ready to battle?";
  $("resultMessage").textContent =
    "Pick a move below to start your next tournament.";

  buttons.forEach(button => button.classList.remove("chosen"));

  updateTournament();
}

$("restartMatchButton").addEventListener("click", restartMatch);


function loadGame() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return {};

    const data = JSON.parse(saved);

    if (
      !data ||
      typeof data !== "object" ||
      !Number.isInteger(data.playerScore) ||
      !Number.isInteger(data.computerScore) ||
      !Number.isInteger(data.currentStreak) ||
      !Number.isInteger(data.bestStreak) ||
      !Number.isInteger(data.round) ||
      !Array.isArray(data.history) ||
      data.playerScore < 0 ||
      data.computerScore < 0 ||
      data.currentStreak < 0 ||
      data.bestStreak < 0 ||
      data.round < 0 ||
      data.history.some(item =>
        !item ||
        !moves[item.player] ||
        !moves[item.computer] ||
        !["win", "lose", "draw"].includes(item.outcome) ||
        !Number.isInteger(item.round) ||
        item.round < 1 ||
        item.round > data.round
      )
    ) {
      return {};
    }

    return data;
  } catch {
    return {};
  }
}

const savedGame = loadGame();

let playerScore = savedGame.playerScore ?? 0;
let computerScore = savedGame.computerScore ?? 0;
let currentStreak = savedGame.currentStreak ?? 0;
let bestStreak = savedGame.bestStreak ?? 0;
let round = savedGame.round ?? 0;
let history = savedGame.history ?? [];

function saveGame() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      playerScore,
      computerScore,
      currentStreak,
      bestStreak,
      round,
      history
    }));
  } catch (error) {
    console.warn("Could not save game progress:", error);
  }
}

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

  $("historyCount").textContent =
    `${history.length} ROUND${history.length === 1 ? "" : "S"}`;

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


function updateStats() {
  const wins = history.filter(item => item.outcome === "win").length;
  const losses = history.filter(item => item.outcome === "lose").length;
  const draws = history.filter(item => item.outcome === "draw").length;

  const total = history.length;
  const decisiveRounds = wins + losses;

  const winRate = decisiveRounds > 0
    ? Math.round((wins / decisiveRounds) * 100)
    : 0;

  $("winPercentage").textContent = `${winRate}%`;
  $("totalWins").textContent = wins;
  $("totalRounds").textContent = total;

  $("winsCount").textContent = wins;
  $("lossesCount").textContent = losses;
  $("drawsCount").textContent = draws;

  // Compare each result against all rounds played.
  [
    ["winsBar", wins],
    ["lossesBar", losses],
    ["drawsBar", draws]
  ].forEach(([id, count]) => {
    $(id).style.width =
      total > 0 ? `${(count / total) * 100}%` : "0%";
  });

  // Display the 10 most recent rounds.
  const chart = $("recentChart");
  chart.replaceChildren();

  const recent = history.slice(0, 10);

  if (recent.length === 0) {
    const empty = document.createElement("p");
    empty.className = "chart-empty";
    empty.textContent = "Play a round to see your performance.";
    chart.append(empty);
    return;
  }

  recent.forEach(item => {
    const column = document.createElement("div");
    column.className = "recent-column";

    const bar = document.createElement("div");
    const resultClass = {
      win: "win-dot",
      lose: "loss-dot",
      draw: "draw-dot"
    }[item.outcome];

    bar.className = `recent-bar ${resultClass}`;
    bar.style.height = "54px";

    const resultName = {
      win: "Win",
      lose: "Loss",
      draw: "Draw"
    }[item.outcome];

    bar.title = `Round ${item.round}: ${resultName}`;
    bar.setAttribute("role", "img");
    bar.setAttribute("aria-label", bar.title);

    const label = document.createElement("span");
    label.className = "recent-round";
    label.textContent = `#${item.round}`;

    column.append(bar, label);
    chart.append(column);
  });
}


function play(player) {
  if (!moves[player] || matchFinished) return;

  const computer = getComputerChoice();
  const outcome = getOutcome(player, computer);

  round++;

  $("playerHand").textContent = moves[player].emoji;
  $("computerHand").textContent = moves[computer].emoji;
  $("playerChoice").textContent = moves[player].name;
  $("computerChoice").textContent = moves[computer].name;

  for (const id of ["playerHand", "computerHand"]) {
    const hand = $(id);
    hand.classList.remove("shake");
    void hand.offsetWidth;
    hand.classList.add("shake");
  }

 if (outcome === "win") {
  playerScore++;
  matchPlayerScore++;
  currentStreak++;
  bestStreak = Math.max(bestStreak, currentStreak);
 } else if (outcome === "lose") {
  computerScore++;
  matchComputerScore++;
  currentStreak = 0;
 } else {
  currentStreak = 0;
 }

 if (
  matchPlayerScore >= MATCH_TARGET ||
  matchComputerScore >= MATCH_TARGET
 ) {
  matchFinished = true;
 }

  history.unshift({ round, player, computer, outcome });

  updateScoreboard();
  showResult(outcome, player, computer);
  renderHistory();
  saveGame();
  updateTournament();
  updateStats();

  buttons.forEach(button => {
    button.classList.toggle(
      "chosen",
      button.dataset.choice === player
    );
  });
}

buttons.forEach(button => {
  button.addEventListener("click", () => play(button.dataset.choice));
});

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
  $("resultMessage").textContent =
    "Pick a move below to start your first round.";

  buttons.forEach(button => button.classList.remove("chosen"));

  updateScoreboard();
  renderHistory();
  updateTournament();
  saveGame();
  updateStats();
});

updateScoreboard();
renderHistory();
updateTournament();
saveGame();
updateStats();

if (round > 0 && history.length > 0) {
  const latest = history[0];

  $("playerHand").textContent = moves[latest.player].emoji;
  $("computerHand").textContent = moves[latest.computer].emoji;
  $("playerChoice").textContent = moves[latest.player].name;
  $("computerChoice").textContent = moves[latest.computer].name;

  showResult(latest.outcome, latest.player, latest.computer);

  buttons.forEach(button => {
    button.classList.toggle(
      "chosen",
      button.dataset.choice === latest.player
    );
  });
}
