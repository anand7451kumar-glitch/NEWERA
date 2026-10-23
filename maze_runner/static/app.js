const COLORS = { wall: "#2b3447", floor: "#12161f", path: "#f7b267", player: "#4ee1c1", goal: "#ff5d73" };
const canvas = document.getElementById("maze"), ctx = canvas.getContext("2d");
const $ = (id) => document.getElementById(id);
let M, pos, moves, best, startTime, timer, showPath, done, cell;

async function load(seed) {
  const size = $("size").value;
  const res = await fetch(`/api/maze?size=${size}` + (seed ? `&seed=${seed}` : ""));
  M = await res.json();
  const sol = await (await fetch(`/api/solve?size=${M.size}&seed=${M.seed}`)).json();
  best = sol.path.length - 1;
  $("seed").textContent = M.seed;
  reset();
}

function reset() {
  pos = [...M.start]; moves = 0; done = false; showPath = null; startTime = null;
  clearInterval(timer); $("moves").textContent = 0; $("time").textContent = "0.0s"; $("message").textContent = "";
  const n = M.grid.length;
  cell = Math.max(8, Math.floor(Math.min(560, window.innerWidth - 32) / n));
  canvas.width = canvas.height = cell * n;
  draw();
}

function draw() {
  M.grid.forEach((row, r) => row.forEach((v, c) => {
    ctx.fillStyle = v ? COLORS.wall : COLORS.floor;
    ctx.fillRect(c * cell, r * cell, cell, cell);
  }));
  if (showPath) { ctx.fillStyle = COLORS.path; showPath.forEach(([r, c]) => ctx.fillRect(c * cell + cell * 0.3, r * cell + cell * 0.3, cell * 0.4, cell * 0.4)); }
  ctx.fillStyle = COLORS.goal; ctx.fillRect(M.end[1] * cell, M.end[0] * cell, cell, cell);
  ctx.fillStyle = COLORS.player; ctx.fillRect(pos[1] * cell, pos[0] * cell, cell, cell);
}

function move(dr, dc) {
  if (done) return;
  const r = pos[0] + dr, c = pos[1] + dc;
  if (M.grid[r]?.[c] !== 0) return;
  if (!startTime) { startTime = Date.now(); timer = setInterval(() => ($("time").textContent = ((Date.now() - startTime) / 1000).toFixed(1) + "s"), 100); }
  pos = [r, c]; $("moves").textContent = ++moves; showPath = null; draw();
  if (r === M.end[0] && c === M.end[1]) win();
}

function win() {
  done = true; clearInterval(timer);
  const secs = ((Date.now() - startTime) / 1000).toFixed(1);
  const perfect = moves === best ? " That's a perfect run!" : ` The shortest route was ${best} moves.`;
  $("message").textContent = `Escaped in ${moves} moves and ${secs}s.${perfect}`;
}

const KEYS = { ArrowUp: [-1, 0], w: [-1, 0], ArrowDown: [1, 0], s: [1, 0], ArrowLeft: [0, -1], a: [0, -1], ArrowRight: [0, 1], d: [0, 1] };
const DIRS = { up: [-1, 0], down: [1, 0], left: [0, -1], right: [0, 1] };
document.addEventListener("keydown", (e) => {
  const d = KEYS[e.key]; if (!d) return;
  e.preventDefault(); move(...d);
});
document.querySelectorAll(".pad button").forEach((b) => (b.onclick = () => move(...DIRS[b.dataset.d])));
$("new").onclick = () => load();
$("restart").onclick = reset;
$("size").onchange = () => load();
$("hint").onclick = async () => {
  if (done) return;
  const res = await fetch(`/api/solve?size=${M.size}&seed=${M.seed}&r=${pos[0]}&c=${pos[1]}`);
  showPath = (await res.json()).path; draw();
};

load();
