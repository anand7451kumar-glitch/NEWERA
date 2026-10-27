const ROWS = 6, COLS = 7;
const $ = (id) => document.getElementById(id);
let board, busy, over, tally = { w: 0, l: 0, d: 0 };
try { tally = JSON.parse(localStorage.getItem("c4-score")) || tally; } catch (e) {}

function showTally() { $("w").textContent = tally.w; $("l").textContent = tally.l; $("d").textContent = tally.d; }
function say(t) { $("status").textContent = t; }

function render(last, line) {
  const focused = document.activeElement && document.activeElement.dataset ? document.activeElement.dataset.c : null;
  const winCells = new Set((line || []).map((p) => p.join()));
  const cols = [];
  for (let c = 0; c < COLS; c++) {
    const b = document.createElement("button");
    b.className = "col"; b.dataset.c = c; b.disabled = over || busy || board[0][c] !== 0;
    b.setAttribute("aria-label", `Drop in column ${c + 1}`);
    b.onclick = () => play(c);
    for (let r = 0; r < ROWS; r++) {
      const cell = document.createElement("div"); cell.className = "cell";
      if (board[r][c]) {
        const p = document.createElement("div");
        p.className = "piece p" + board[r][c] + (last && last[0] === r && last[1] === c ? " drop" : "") + (winCells.has(r + "," + c) ? " win" : "");
        p.style.setProperty("--r", r);
        cell.appendChild(p);
      }
      b.appendChild(cell);
    }
    cols.push(b);
  }
  $("board").replaceChildren(...cols);
  if (focused !== null) { const f = $("board").querySelector(`[data-c="${focused}"]`); if (f && !f.disabled) f.focus(); }
}

async function aiTurn() {
  busy = true; render(); say("The AI is thinking...");
  try {
    const res = await fetch("/api/ai", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ board, level: $("level").value }) });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Server error");
    board = data.board;
    if (data.winner || data.draw) {
      over = true;
      if (data.winner === 1) { tally.w++; say("You win!"); } else if (data.winner === 2) { tally.l++; say("The AI wins."); } else { tally.d++; say("It's a draw."); }
      try { localStorage.setItem("c4-score", JSON.stringify(tally)); } catch (e) {}
      showTally();
    } else say("Your turn.");
    busy = false; render(data.row === null ? null : [data.row, data.col], data.line);
  } catch (e) { busy = false; say(e.message + " Is app.py running?"); render(); }
}

async function play(c) {
  if (busy || over) return;
  let r = ROWS - 1;
  while (r >= 0 && board[r][c] !== 0) r--;
  if (r < 0) return;
  board[r][c] = 1;
  render([r, c]);
  await aiTurn();
}

function newGame() {
  board = Array.from({ length: ROWS }, () => Array(COLS).fill(0)); over = false; busy = false;
  render(); showTally(); say("Your turn.");
  if ($("first").value === "ai") aiTurn();
}

document.addEventListener("keydown", (e) => { if (/^[1-7]$/.test(e.key) && !e.target.matches("select")) play(Number(e.key) - 1); });
$("new").onclick = newGame;
newGame();
