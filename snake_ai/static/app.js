const W = 20, H = 20, CELL = 20;
const canvas = document.getElementById("board"), ctx = canvas.getContext("2d");
const $ = (id) => document.getElementById(id);
const DIRS = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] };
const KEYS = { ArrowUp: "up", w: "up", ArrowDown: "down", s: "down", ArrowLeft: "left", a: "left", ArrowRight: "right", d: "right" };
let snake, dir, nextDir, food, score, running, auto = false, best = 0, run = 0;

try { best = Number(localStorage.getItem("snake-best")) || 0; } catch (e) {}
$("best").textContent = best;

function reset() {
  snake = [[10, 10], [9, 10], [8, 10]]; dir = nextDir = "right"; score = 0; $("score").textContent = 0;
  placeFood(); draw();
}

function placeFood() {
  const taken = new Set(snake.map((p) => p.join()));
  const free = [];
  for (let x = 0; x < W; x++) for (let y = 0; y < H; y++) if (!taken.has(x + "," + y)) free.push([x, y]);
  food = free.length ? free[Math.floor(Math.random() * free.length)] : null;
}

function draw() {
  ctx.fillStyle = "#0a120d"; ctx.fillRect(0, 0, canvas.width, canvas.height);
  if (food) { ctx.fillStyle = "#ff6b6b"; ctx.beginPath(); ctx.arc(food[0] * CELL + CELL / 2, food[1] * CELL + CELL / 2, CELL * 0.38, 0, 7); ctx.fill(); }
  snake.forEach(([x, y], i) => { ctx.fillStyle = i ? "#3fb950" : "#7ee787"; ctx.fillRect(x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2); });
}

async function chooseDirection() {
  if (!auto) return;
  try {
    const res = await fetch("/api/ai", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ width: W, height: H, snake, food }) });
    const data = await res.json();
    if (data.move) nextDir = data.move;
  } catch (e) { $("message").textContent = "Can't reach the server. Is app.py running?"; }
}

function step() {
  const [dx, dy] = DIRS[nextDir]; dir = nextDir;
  const head = [snake[0][0] + dx, snake[0][1] + dy];
  const eating = food && head[0] === food[0] && head[1] === food[1];
  const body = (eating ? snake : snake.slice(0, -1)).map((p) => p.join());
  if (head[0] < 0 || head[0] >= W || head[1] < 0 || head[1] >= H || body.includes(head.join())) return end(false);
  snake.unshift(head);
  if (eating) { score++; $("score").textContent = score; placeFood(); if (!food) return end(true); } else snake.pop();
  draw();
}

function end(won) {
  running = false;
  if (score > best) { best = score; $("best").textContent = best; try { localStorage.setItem("snake-best", best); } catch (e) {} }
  $("message").textContent = (won ? "The snake filled the board! " : "Game over. ") + `Score ${score}. Press Start to play again.`;
  $("start").textContent = "Start";
}

async function loop(id) {
  while (running && id === run) {
    const t0 = performance.now();
    await chooseDirection();
    if (!running || id !== run) return;
    step();
    const wait = Number($("speed").value) - (performance.now() - t0);
    await new Promise((r) => setTimeout(r, Math.max(0, wait)));
  }
}

function start() { reset(); running = true; run++; $("message").textContent = ""; $("start").textContent = "Restart"; loop(run); }

$("start").onclick = start;
$("auto").onclick = () => { auto = !auto; $("auto").setAttribute("aria-pressed", auto); $("auto").textContent = "Autopilot: " + (auto ? "on" : "off"); };
document.addEventListener("keydown", (e) => {
  const d = KEYS[e.key]; if (!d) return;
  e.preventDefault();
  const opposite = { up: "down", down: "up", left: "right", right: "left" };
  if (!running) start();
  if (!auto && d !== opposite[dir]) nextDir = d;
});
reset();
