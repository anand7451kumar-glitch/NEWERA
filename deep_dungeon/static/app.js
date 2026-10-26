const T = 16, canvas = document.getElementById("map"), ctx = canvas.getContext("2d");
const $ = (id) => document.getElementById(id);
const KEYS = { ArrowUp: [0, -1], w: [0, -1], ArrowDown: [0, 1], s: [0, 1], ArrowLeft: [-1, 0], a: [-1, 0], ArrowRight: [1, 0], d: [1, 0], " ": [0, 0] };
const GLYPH = { r: "#c9b79c", g: "#7fd36e", o: "#ff6b6b", "!": "#ff7ac6", "/": "#5ec8ff" };
let run = null, busy = false;

async function api(path, body) {
  const res = await fetch(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Server error");
  return data;
}

function letter(ch, x, y, color) {
  ctx.fillStyle = color; ctx.fillText(ch, x * T + T / 2, y * T + T / 2 + 1);
}

function draw(s) {
  ctx.fillStyle = "#080a12"; ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.font = "bold 14px 'Courier New', monospace"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
  for (let y = 0; y < s.h; y++) for (let x = 0; x < s.w; x++) {
    const ch = s.tiles[y][x]; if (ch === " ") continue;
    const lit = s.visible[y][x] === "1";
    if (ch === "#") { ctx.fillStyle = lit ? "#3b4772" : "#1f2641"; ctx.fillRect(x * T, y * T, T, T); }
    else {
      ctx.fillStyle = lit ? "#1a1f33" : "#10131f"; ctx.fillRect(x * T, y * T, T, T);
      if (ch === ">") letter(">", x, y, lit ? "#ff9f43" : "#8a5a2a");
      else { ctx.fillStyle = lit ? "#2c3452" : "#1a1f33"; ctx.fillRect(x * T + 7, y * T + 7, 2, 2); }
    }
  }
  s.items.forEach((i) => letter(i.g, i.x, i.y, GLYPH[i.g]));
  s.monsters.forEach((m) => letter(m.g, m.x, m.y, GLYPH[m.g]));
  letter("@", s.player[0], s.player[1], "#5eead4");
  $("hp").textContent = `${s.hp}/${s.max_hp}`; $("atk").textContent = s.atk; $("depth").textContent = s.depth;
  $("kills").textContent = s.kills; $("score").textContent = s.score;
  $("log").replaceChildren(...s.log.map((t) => Object.assign(document.createElement("li"), { textContent: t })));
}

async function newGame() {
  const d = await api("/api/new"); run = d.run; draw(d.state);
}
async function go(dx, dy) {
  if (busy || !run) return; busy = true;
  try { draw(await api("/api/move", { run, dx, dy })); } catch (e) { $("log").textContent = e.message; run = null; }
  busy = false;
}

document.addEventListener("keydown", (e) => { const m = KEYS[e.key]; if (m) { e.preventDefault(); go(...m); } });
document.querySelectorAll("[data-m]").forEach((b) => (b.onclick = () => go(...b.dataset.m.split(",").map(Number))));
$("new").onclick = newGame;
newGame();
