const $ = (id) => document.getElementById(id);
let board, initial, n, moves, hinted, won;

async function load() {
  const data = await (await fetch(`/api/new?size=${$("size").value}`)).json();
  initial = data.board.map((r) => [...r]);
  $("seed").textContent = data.seed;
  reset();
}

function reset() {
  board = initial.map((r) => [...r]); n = board.length; moves = 0; hinted = null; won = false;
  $("message").textContent = ""; render();
}

function press(r, c) {
  for (const [dr, dc] of [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]]) {
    const a = r + dr, b = c + dc;
    if (a >= 0 && a < n && b >= 0 && b < n) board[a][b] ^= 1;
  }
}

function render() {
  const grid = $("grid");
  grid.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
  grid.replaceChildren();
  board.forEach((row, r) => row.forEach((v, c) => {
    const b = document.createElement("button");
    b.className = "cell" + (v ? " on" : "") + (hinted && hinted[0] === r && hinted[1] === c ? " hint" : "");
    b.setAttribute("aria-label", `Row ${r + 1}, column ${c + 1}, ${v ? "on" : "off"}`);
    b.onclick = () => {
      if (won) return;
      press(r, c); moves++; hinted = null;
      if (board.every((row) => row.every((x) => !x))) { won = true; $("message").textContent = `Lights out in ${moves} moves!`; }
      render();
    };
    grid.appendChild(b);
  }));
  $("moves").textContent = moves;
}

$("hint").onclick = async () => {
  if (won) return;
  const res = await fetch("/api/hint", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ board }) });
  const data = await res.json();
  if (!res.ok) { $("message").textContent = data.error; return; }
  hinted = data.presses[0]; render();
};
$("new").onclick = load; $("reset").onclick = reset; $("size").onchange = load;
load();
