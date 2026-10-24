const W = 640, H = 480, MIN_WALL = 14, MAX_WALLS = 30, START = [40, 440], TARGET = [600, 60], TARGET_R = 18;
const PRESETS = {
  wall: [[300, 120, 16, 360]],
  maze: [[160, 0, 16, 340], [320, 140, 16, 340], [480, 0, 16, 340]],
};
const COLORS = { wall: "#4b5a82", rocket: "#b6a6ff", best: "#5eead4", goal: "#ffd166", crash: "#ff6b81" };
const sky = document.getElementById("sky"), ctx = sky.getContext("2d");
const chart = document.getElementById("chart"), cctx = chart.getContext("2d");
const $ = (id) => document.getElementById(id);

let walls = PRESETS.wall.map((r) => [...r]);
let run = null, history = [], evolving = false, busy = false, drag = null, token = 0;

// ---------- server calls ----------
async function api(path, body) {
  const res = await fetch(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Server error");
  return data;
}

// ---------- drawing ----------
function drawWorld() {
  ctx.fillStyle = "#060812"; ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = COLORS.wall;
  walls.forEach(([x, y, w, h]) => ctx.fillRect(x, y, w, h));
  if (drag) { ctx.strokeStyle = "#fff"; ctx.setLineDash([6, 4]); const [x, y, w, h] = dragRect(); ctx.strokeRect(x, y, w, h); ctx.setLineDash([]); }
  ctx.fillStyle = "#8e97b5"; ctx.beginPath(); ctx.arc(START[0], START[1], 6, 0, 7); ctx.fill();
  const g = ctx.createRadialGradient(...TARGET, 2, ...TARGET, TARGET_R * 1.8);
  g.addColorStop(0, "#ffd166"); g.addColorStop(0.5, "rgba(255,209,102,.5)"); g.addColorStop(1, "rgba(255,209,102,0)");
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(...TARGET, TARGET_R * 1.8, 0, 7); ctx.fill();
  ctx.fillStyle = COLORS.goal; ctx.beginPath(); ctx.arc(...TARGET, TARGET_R * 0.6, 0, 7); ctx.fill();
}

function drawRockets(rep, f) {
  const order = rep.paths.map((_, i) => i).filter((i) => i !== rep.best).concat(rep.best);
  for (const i of order) {
    const path = rep.paths[i], last = path.length - 1, idx = Math.min(f, last);
    const isBest = i === rep.best, done = f >= last;
    ctx.strokeStyle = isBest ? COLORS.best : rep.status[i] === "goal" ? COLORS.goal : COLORS.rocket;
    ctx.globalAlpha = isBest ? 1 : 0.55; ctx.lineWidth = isBest ? 2.5 : 1.2;
    ctx.beginPath();
    for (let k = Math.max(0, idx - 14); k <= idx; k++) k === Math.max(0, idx - 14) ? ctx.moveTo(...path[k]) : ctx.lineTo(...path[k]);
    ctx.stroke();
    ctx.fillStyle = done && rep.status[i] === "crash" ? COLORS.crash : ctx.strokeStyle;
    ctx.beginPath(); ctx.arc(...path[idx], isBest ? 4 : 2.5, 0, 7); ctx.fill();
  }
  ctx.globalAlpha = 1; ctx.lineWidth = 1;
}

function drawFinal(rep) {
  drawWorld();
  ctx.lineWidth = 1; ctx.globalAlpha = 0.18; ctx.strokeStyle = COLORS.rocket;
  rep.paths.forEach((p, i) => { if (i === rep.best) return; ctx.beginPath(); p.forEach((pt, k) => (k ? ctx.lineTo(...pt) : ctx.moveTo(...pt))); ctx.stroke(); });
  ctx.globalAlpha = 1; ctx.strokeStyle = COLORS.best; ctx.lineWidth = 3;
  ctx.beginPath(); rep.paths[rep.best].forEach((pt, k) => (k ? ctx.lineTo(...pt) : ctx.moveTo(...pt))); ctx.stroke(); ctx.lineWidth = 1;
}

function drawChart() {
  cctx.clearRect(0, 0, chart.width, chart.height);
  cctx.strokeStyle = "#2a3250"; cctx.beginPath(); cctx.moveTo(0, chart.height - 0.5); cctx.lineTo(chart.width, chart.height - 0.5); cctx.stroke();
  cctx.fillStyle = "#8e97b5"; cctx.font = "12px sans-serif"; cctx.fillText("% of rockets reaching the target, per generation", 8, 14);
  if (history.length < 2) return;
  const n = Math.max(history.length - 1, 40), pad = 22;
  cctx.strokeStyle = COLORS.best; cctx.lineWidth = 2; cctx.beginPath();
  history.forEach((h, i) => { const x = (i / n) * chart.width, y = chart.height - 4 - (h.goal_pct / 100) * (chart.height - pad - 4); i ? cctx.lineTo(x, y) : cctx.moveTo(x, y); });
  cctx.stroke(); cctx.lineWidth = 1;
}

function playback(rep, myToken) {
  const perFrame = Number($("speed").value);
  if (!perFrame) { drawFinal(rep); return Promise.resolve(); }
  return new Promise((resolve) => {
    let f = 0;
    const maxLen = Math.max(...rep.paths.map((p) => p.length));
    (function frame() {
      if (myToken !== token) return resolve();
      drawWorld(); drawRockets(rep, f);
      f += perFrame;
      f - perFrame < maxLen + 6 ? requestAnimationFrame(frame) : resolve();
    })();
  });
}

// ---------- evolution loop ----------
async function stepOnce() {
  if (busy) return;
  busy = true;
  const myToken = token;
  try {
    if (!run) { run = (await api("/api/new", { walls })).run; history = []; }
    const rep = await api("/api/step", { run });
    if (myToken !== token) return;
    history.push(rep);
    $("gen").textContent = rep.gen + 1; $("reached").textContent = rep.goal_pct + "%";
    drawChart(); say(rep);
    await playback(rep, myToken);
  } catch (e) { $("message").textContent = e.message; evolving = false; run = null; syncButton(); }
  finally { busy = false; }
}

function say(rep) {
  let m = "";
  if (rep.closest >= 9999) m = "There is no route to the target. Undo or clear a wall.";
  else if (rep.goal_pct >= 80) m = "The flock has learned the route!";
  else if (rep.goal_pct > 0) m = `${rep.goal_pct}% reached the target. Their children inherit the route.`;
  else m = "Nobody has reached the target yet. Keep evolving.";
  $("message").textContent = m;
}

async function loop() { while (evolving) { await stepOnce(); if (!busy && !run) break; } }
function syncButton() { $("evolve").textContent = evolving ? "Pause" : "Evolve"; }

function wallsChanged() {
  token++; run = null; history = []; evolving = false; busy = false;
  $("gen").textContent = 0; $("reached").textContent = "0%"; $("message").textContent = "Press Evolve to start from scratch.";
  syncButton(); drawWorld(); drawChart();
}

// ---------- controls ----------
$("evolve").onclick = () => { evolving = !evolving; syncButton(); if (evolving) loop(); };
$("step").onclick = () => { evolving = false; syncButton(); stepOnce(); };
$("reset").onclick = wallsChanged;
$("undo").onclick = () => { walls.pop(); wallsChanged(); };
$("clear").onclick = () => { walls = []; wallsChanged(); };
document.querySelectorAll("[data-preset]").forEach((b) => (b.onclick = () => { walls = PRESETS[b.dataset.preset].map((r) => [...r]); wallsChanged(); }));

// ---------- drawing walls with mouse or finger ----------
function point(e) {
  const b = sky.getBoundingClientRect();
  return [Math.max(0, Math.min(W, (e.clientX - b.left) * W / b.width)), Math.max(0, Math.min(H, (e.clientY - b.top) * H / b.height))];
}
function dragRect() {
  const [x0, y0] = drag.from, [x1, y1] = drag.to;
  return [Math.round(Math.min(x0, x1)), Math.round(Math.min(y0, y1)), Math.max(MIN_WALL, Math.round(Math.abs(x1 - x0))), Math.max(MIN_WALL, Math.round(Math.abs(y1 - y0)))];
}
sky.addEventListener("pointerdown", (e) => { sky.setPointerCapture(e.pointerId); drag = { from: point(e), to: point(e) }; drawWorld(); });
sky.addEventListener("pointermove", (e) => { if (drag) { drag.to = point(e); drawWorld(); } });
sky.addEventListener("pointerup", () => {
  if (!drag) return;
  if (walls.length < MAX_WALLS) walls.push(dragRect());
  drag = null; wallsChanged();
});

drawWorld(); drawChart();
