const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const scoreEl = document.getElementById("score");
const bestEl = document.getElementById("best");
const comboEl = document.getElementById("combo");
const overlay = document.getElementById("overlay");
const title = document.getElementById("overlayTitle");
const text = document.getElementById("overlayText");
const eyebrow = document.getElementById("eyebrow");
const startBtn = document.getElementById("startBtn");

const W = canvas.width;
const H = canvas.height;
const lanes = [W / 6, W / 2, W * 5 / 6];

let playerLane = 1;
let obstacles = [];
let particles = [];
let score = 0;
let best = Number(localStorage.getItem("echoBest")) || 0;
let combo = 1;
let running = false;
let lastTime = 0;
let spawnTimer = 0;
let elapsed = 0;
let flash = 0;

bestEl.textContent = format(best);

function format(n) {
  return String(Math.floor(n)).padStart(5, "0");
}

function startGame() {
  score = 0;
  combo = 1;
  playerLane = 1;
  obstacles = [];
  particles = [];
  elapsed = 0;
  spawnTimer = 0;
  flash = 0;
  lastTime = performance.now();
  running = true;

  scoreEl.textContent = format(0);
  comboEl.textContent = "x1";
  overlay.classList.add("hidden");

  requestAnimationFrame(loop);
}

function endGame() {
  running = false;

  if (score > best) {
    best = score;
    localStorage.setItem("echoBest", best);
    bestEl.textContent = format(best);
  }

  eyebrow.textContent = "SIGNAL LOST";
  title.innerHTML = "GAME<br><span>OVER.</span>";
  text.textContent = `You scored ${format(score)}. Your best is ${format(best)}.`;
  startBtn.innerHTML = "TRY AGAIN <span>↗</span>";
  overlay.classList.remove("hidden");
}

function move(direction) {
  if (!running) return;

  const next = Math.max(0, Math.min(2, playerLane + direction));

  if (next !== playerLane) {
    playerLane = next;
    createBurst(lanes[playerLane], H - 90, 8, "#48f4e4");
  }
}

document.addEventListener("keydown", event => {
  if (event.key === "ArrowLeft" || event.key.toLowerCase() === "a") {
    event.preventDefault();
    move(-1);
  }

  if (event.key === "ArrowRight" || event.key.toLowerCase() === "d") {
    event.preventDefault();
    move(1);
  }

  if (event.key === " " && !running) {
    startGame();
  }
});

canvas.addEventListener("pointerdown", event => {
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;

  move(x < rect.width / 2 ? -1 : 1);
});

startBtn.addEventListener("click", startGame);

function createBurst(x, y, amount, color) {
  for (let i = 0; i < amount; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = 1 + Math.random() * 4;

    particles.push({
      x, y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: 1,
      color
    });
  }
}

function spawnObstacle() {
  const lane = Math.floor(Math.random() * 3);

  obstacles.push({
    lane,
    y: -35,
    size: 19,
    speed: 240 + Math.min(elapsed * 8, 300),
    passed: false
  });
}

function update(dt) {
  elapsed += dt;

  const spawnRate = Math.max(0.42, 0.95 - elapsed * 0.008);
  spawnTimer += dt;

  if (spawnTimer >= spawnRate) {
    spawnObstacle();
    spawnTimer = 0;
  }

  const playerY = H - 90;

  for (const obstacle of obstacles) {
    obstacle.y += obstacle.speed * dt;

    const sameLane = obstacle.lane === playerLane;
    const distance = Math.abs(obstacle.y - playerY);

    if (sameLane && distance < 31) {
      createBurst(lanes[playerLane], playerY, 35, "#ff4d9d");
      flash = 1;
      endGame();
      return;
    }

    if (!obstacle.passed && obstacle.y > playerY + 35) {
      obstacle.passed = true;
      score += 100 * combo;
      combo = Math.min(combo + 1, 8);

      scoreEl.textContent = format(score);
      comboEl.textContent = "x" + combo;
    }
  }

  obstacles = obstacles.filter(o => o.y < H + 50);

  for (const p of particles) {
    p.x += p.vx;
    p.y += p.vy;
    p.life -= dt * 1.8;
  }

  particles = particles.filter(p => p.life > 0);

  flash = Math.max(0, flash - dt * 2);
}

function drawBackground() {
  ctx.fillStyle = "#090d15";
  ctx.fillRect(0, 0, W, H);

  // Background grid
  ctx.strokeStyle = "#182433";
  ctx.lineWidth = 1;

  for (let x = 0; x <= W; x += 45) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, H);
    ctx.stroke();
  }

  for (let y = 0; y <= H; y += 45) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(W, y);
    ctx.stroke();
  }

  // Lane dividers
  for (let i = 1; i < 3; i++) {
    const x = (W / 3) * i;

    ctx.setLineDash([5, 12]);
    ctx.strokeStyle = "#344454";
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, H);
    ctx.stroke();
  }

  ctx.setLineDash([]);

  // Lane glow
  const laneX = lanes[playerLane];

  const glow = ctx.createRadialGradient(
    laneX, H - 90, 5,
    laneX, H - 90, 140
  );

  glow.addColorStop(0, "#48f4e418");
  glow.addColorStop(1, "#48f4e400");

  ctx.fillStyle = glow;
  ctx.fillRect(0, H - 230, W, 230);
}

function drawPlayer() {
  const x = lanes[playerLane];
  const y = H - 90;

  ctx.save();
  ctx.translate(x, y);

  ctx.shadowBlur = 25;
  ctx.shadowColor = "#48f4e4";

  ctx.fillStyle = "#48f4e4";
  ctx.beginPath();
  ctx.moveTo(0, -23);
  ctx.lineTo(20, 0);
  ctx.lineTo(0, 23);
  ctx.lineTo(-20, 0);
  ctx.closePath();
  ctx.fill();

  ctx.shadowBlur = 0;
  ctx.fillStyle = "#081418";
  ctx.beginPath();
  ctx.arc(0, 0, 6, 0, Math.PI * 2);
  ctx.fill();

  ctx.restore();
}

function drawObstacles() {
  for (const o of obstacles) {
    const x = lanes[o.lane];

    ctx.save();
    ctx.translate(x, o.y);
    ctx.rotate(Math.PI / 4);

    ctx.shadowBlur = 20;
    ctx.shadowColor = "#ff4d9d";
    ctx.fillStyle = "#ff4d9d";

    ctx.fillRect(-o.size / 2, -o.size / 2, o.size, o.size);

    ctx.restore();
  }
}

function drawParticles() {
  for (const p of particles) {
    ctx.globalAlpha = Math.max(0, p.life);
    ctx.fillStyle = p.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.globalAlpha = 1;
}

function draw() {
  drawBackground();
  drawObstacles();
  drawParticles();

  if (running) drawPlayer();

  if (flash > 0) {
    ctx.fillStyle = `rgba(255, 77, 157, ${flash * 0.15})`;
    ctx.fillRect(0, 0, W, H);
  }

  // Arena label
  ctx.fillStyle = "#566477";
  ctx.font = "11px monospace";
  ctx.fillText("SECTOR 01 / REFLEX TEST", 22, 28);
}

function loop(timestamp) {
  if (!running) return;

  const dt = Math.min((timestamp - lastTime) / 1000, 0.04);
  lastTime = timestamp;

  update(dt);
  draw();

  if (running) requestAnimationFrame(loop);
}

// Initial screen
drawBackground();
draw();
bestEl.textContent = format(best);