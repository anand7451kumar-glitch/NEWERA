
const canvas = document.getElementById("world");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;

let day = 1;
let running = true;
let speed = 1;
let timer = 0;
let weather = "sun";
let water = 75;
let sunlight = 80;
let health = 100;
let gameOver = false;
let rainDays = 0;

let plants = [];
let rabbits = [];
let foxes = [];
let butterflies = [];
let clouds = [];
let particles = [];

let bestDay = Number(localStorage.getItem("tinyWildBest") || 0);

const random = (min, max) => Math.random() * (max - min) + min;

function islandPoint() {
  const angle = random(0, Math.PI * 2);
  const radius = Math.sqrt(Math.random());
  return {
    x: 450 + Math.cos(angle) * radius * 350,
    y: 280 + Math.sin(angle) * radius * 205
  };
}

function makeCreature(type) {
  const p = islandPoint();
  return {
    x: p.x,
    y: p.y,
    dx: random(-0.7, 0.7),
    dy: random(-0.7, 0.7),
    phase: random(0, 10),
    type
  };
}

function createWorld() {
  day = 1;
  water = 75;
  sunlight = 80;
  health = 100;
  weather = "sun";
  rainDays = 0;
  gameOver = false;
  running = true;
  speed = 1;

  plants = [];
  rabbits = [];
  foxes = [];
  butterflies = [];
  clouds = [];
  particles = [];

  for (let i = 0; i < 35; i++) plants.push(makeCreature("plant"));
  for (let i = 0; i < 8; i++) rabbits.push(makeCreature("rabbit"));
  for (let i = 0; i < 2; i++) foxes.push(makeCreature("fox"));
  for (let i = 0; i < 7; i++) butterflies.push(makeCreature("butterfly"));
  for (let i = 0; i < 5; i++) clouds.push({
    x: random(0, W),
    y: random(20, 150),
    size: random(20, 42),
    speed: random(0.1, 0.3)
  });

  addLog("🌱 A fresh ecosystem has begun.");
  updateUI();
  draw();
}

function addLog(message) {
  const log = document.getElementById("log");
  const entry = document.createElement("p");
  entry.textContent = `DAY ${String(day).padStart(2, "0")} · ${message}`;
  log.prepend(entry);

  while (log.children.length > 15) {
    log.removeChild(log.lastChild);
  }
}

function addAction(action) {
  if (gameOver) return;

  if (action === "plant") {
    if (plants.length >= 100) return addLog("🌳 The island has plenty of plants already.");
    plants.push(makeCreature("plant"));
    water = Math.max(0, water - 1);
    addLog("🌱 A new plant takes root.");
  }

  if (action === "rabbit") {
    if (rabbits.length >= 30) return addLog("🐇 Too many rabbits! The island needs balance.");
    rabbits.push(makeCreature("rabbit"));
    addLog("🐇 A rabbit joins the island.");
  }

  if (action === "fox") {
    if (foxes.length >= 12) return addLog("🦊 The island cannot support more foxes.");
    foxes.push(makeCreature("fox"));
    addLog("🦊 A fox enters the ecosystem.");
  }

  if (action === "rain") {
    water = Math.min(100, water + 30);
    rainDays = 2;
    weather = "rain";
    addLog("🌧️ You summoned rain. The island drinks it in.");
  }

  updateUI();
}

document.querySelectorAll("[data-action]").forEach(button => {
  button.addEventListener("click", () => {
    addAction(button.dataset.action);
  });
});

document.getElementById("playBtn").addEventListener("click", () => {
  if (gameOver) return;
  running = !running;
  document.getElementById("playBtn").textContent = running ? "Ⅱ Pause" : "▶ Resume";
});

document.getElementById("speedBtn").addEventListener("click", () => {
  speed = speed === 1 ? 2 : speed === 2 ? 4 : 1;
  document.getElementById("speedBtn").textContent = `Speed: ${speed}×`;
});

document.getElementById("restartBtn").addEventListener("click", () => {
  if (confirm("Start a brand-new island? Your current island will be lost.")) {
    createWorld();
    document.getElementById("playBtn").textContent = "Ⅱ Pause";
    document.getElementById("speedBtn").textContent = "Speed: 1×";
  }
});

function chooseWeather() {
  if (rainDays > 0) {
    rainDays--;
    weather = "rain";
    return;
  }

  const roll = Math.random();
  if (roll < 0.18) weather = "rain";
  else if (roll < 0.30) weather = "cloud";
  else if (roll < 0.38) weather = "drought";
  else weather = "sun";
}

function simulateDay() {
  if (gameOver) return;

  day++;
  chooseWeather();

  if (weather === "rain") {
    water = Math.min(100, water + 15);
    sunlight = Math.max(20, sunlight - 12);
  } else if (weather === "drought") {
    water = Math.max(0, water - 16);
    sunlight = Math.min(100, sunlight + 12);
  } else if (weather === "cloud") {
    water = Math.min(100, water + 3);
    sunlight = Math.max(30, sunlight - 5);
  } else {
    water = Math.max(0, water - 5);
    sunlight = Math.min(100, sunlight + 5);
  }

  // Plants grow when there is enough water and sunlight.
  const growth = water > 25 && sunlight > 30 ? 0.35 : 0.08;
  if (Math.random() < growth && plants.length < 100) {
    plants.push(makeCreature("plant"));
  }

  // Rabbits eat plants.
  const foodAvailable = plants.length > 8;
  if (foodAvailable && rabbits.length > 0) {
    const eaten = Math.min(plants.length - 5, Math.ceil(rabbits.length * 0.45));
    plants.splice(0, Math.max(0, eaten));
  }

  if (rabbits.length > 0 && plants.length < 8 && Math.random() < 0.7) {
    rabbits.splice(Math.floor(Math.random() * rabbits.length), 1);
    addLog("🥀 A rabbit has left due to lack of food.");
  } else if (plants.length > 20 && rabbits.length < 25 && Math.random() < 0.45) {
    rabbits.push(makeCreature("rabbit"));
    addLog("🐇 A new rabbit was born.");
  }

  // Foxes hunt rabbits.
  if (foxes.length > 0 && rabbits.length > 0 && Math.random() < 0.7) {
    const hunted = Math.min(foxes.length, rabbits.length);
    for (let i = 0; i < hunted; i++) {
      if (Math.random() < 0.6 && rabbits.length > 0) rabbits.pop();
    }
  }

  if (rabbits.length < 3 && foxes.length > 0 && Math.random() < 0.5) {
    foxes.pop();
    addLog("🦊 A fox leaves to find food elsewhere.");
  } else if (rabbits.length > 8 && foxes.length < 8 && Math.random() < 0.2) {
    foxes.push(makeCreature("fox"));
    addLog("🦊 A fox has settled on the island.");
  }

  // Butterflies thrive when plants are plentiful.
  if (plants.length > 15 && butterflies.length < 20 && Math.random() < 0.4) {
    butterflies.push(makeCreature("butterfly"));
  }
  if (plants.length < 5 && butterflies.length > 0 && Math.random() < 0.6) {
    butterflies.pop();
  }

  calculateHealth();

  if (day % 5 === 0) {
    addLog(`📅 Day ${day}: ${plants.length} plants, ${rabbits.length} rabbits, ${foxes.length} foxes.`);
  }

  if (day >= 100) {
    gameOver = true;
    running = false;
    addLog("🏆 100 days survived! Your island is a success.");
  }

  updateUI();
}

function calculateHealth() {
  const plantScore = Math.min(plants.length / 35, 1) * 35;
  const rabbitScore = Math.min(rabbits.length / 10, 1) * 25;
  const foxScore = foxes.length > 0 ? Math.min(foxes.length / 3, 1) * 15 : 0;
  const butterflyScore = Math.min(butterflies.length / 8, 1) * 10;
  const waterScore = water > 25 ? 15 : water * 0.6;

  health = Math.round(plantScore + rabbitScore + foxScore + butterflyScore + waterScore);
  health = Math.max(0, Math.min(100, health));

  if (health < 15 && day > 5) {
    addLog("⚠️ Ecosystem warning: biodiversity is critically low.");
  }

  if (health === 0 || (plants.length === 0 && rabbits.length === 0 && foxes.length === 0)) {
    gameOver = true;
    running = false;
    addLog("💀 The ecosystem has collapsed. Restart to try again.");
  }

  if (day > bestDay) {
    bestDay = day;
    localStorage.setItem("tinyWildBest", bestDay);
  }
}

function updateUI() {
  document.getElementById("day").textContent = `DAY ${String(day).padStart(2, "0")}`;
  document.getElementById("health").textContent = health;
  document.getElementById("healthBar").style.width = `${health}%`;

  const healthText = health > 75 ? "Your ecosystem is flourishing." :
    health > 45 ? "The ecosystem is doing okay." :
    health > 20 ? "Your island needs attention." : "Critical! The ecosystem is struggling.";

  document.getElementById("healthText").textContent = healthText;

  document.getElementById("plants").textContent = plants.length;
  document.getElementById("rabbits").textContent = rabbits.length;
  document.getElementById("foxes").textContent = foxes.length;
  document.getElementById("butterflies").textContent = butterflies.length;

  document.getElementById("waterValue").textContent = `${Math.round(water)}%`;
  document.getElementById("sunValue").textContent = `${Math.round(sunlight)}%`;

  const biodiversity = Math.round(
    Math.min(100, (plants.length + rabbits.length * 3 + foxes.length * 5 + butterflies.length * 2) / 1.5)
  );
  document.getElementById("bioValue").textContent = `${biodiversity}%`;

  document.getElementById("waterBar").style.width = `${water}%`;
  document.getElementById("sunBar").style.width = `${sunlight}%`;
  document.getElementById("bioBar").style.width = `${biodiversity}%`;

  document.getElementById("missionBar").style.width = `${Math.min(day, 100)}%`;
  document.getElementById("missionText").textContent = `${Math.min(day, 100)} / 100 days`;

  const weatherNames = {
    sun: "☀️ Sunny",
    rain: "🌧️ Rainy",
    cloud: "☁️ Cloudy",
    drought: "🔥 Drought"
  };
  document.getElementById("weather").textContent = weatherNames[weather];

  document.getElementById("world-message").textContent =
    gameOver ? (day >= 100 ? "🏆 Your island survived 100 days!" : "The ecosystem has collapsed. Restart to try again.") :
    health > 75 ? "Everything is growing beautifully." :
    health > 40 ? "Your island needs a little care." :
    "The balance of nature is in danger.";
}

// Draw the island and its inhabitants.
function drawBackground() {
  ctx.fillStyle = "#a8d69a";
  ctx.fillRect(0, 0, W, H);

  // Island shape.
  ctx.fillStyle = "#d6c58e";
  ctx.beginPath();
  ctx.ellipse(450, 280, 370, 225, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#75b77c";
  ctx.beginPath();
  ctx.ellipse(450, 270, 350, 210, 0, 0, Math.PI * 2);
  ctx.fill();

  // Pond.
  ctx.fillStyle = "#6bbbd0";
  ctx.beginPath();
  ctx.ellipse(520, 300, 105, 60, -0.3, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#a4e0df";
  ctx.beginPath();
  ctx.ellipse(500, 286, 34, 8, -0.3, 0, Math.PI * 2);
  ctx.fill();

  // Paths.
  ctx.strokeStyle = "#b6a77c";
  ctx.lineWidth = 15;
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.moveTo(180, 380);
  ctx.quadraticCurveTo(350, 340, 410, 390);
  ctx.quadraticCurveTo(490, 420, 600, 365);
  ctx.stroke();

  // Clouds.
  clouds.forEach(cloud => {
    ctx.fillStyle = weather === "rain" ? "#9daeb1" : "#eaf5df";
    ctx.globalAlpha = 0.65;
    ctx.beginPath();
    ctx.arc(cloud.x, cloud.y, cloud.size, 0, Math.PI * 2);
    ctx.arc(cloud.x + cloud.size, cloud.y - 8, cloud.size * 0.8, 0, Math.PI * 2);
    ctx.arc(cloud.x + cloud.size * 1.6, cloud.y, cloud.size * 0.9, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1;
  });
}

function drawPlant(p) {
  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.fillStyle = "#276d3d";
  ctx.fillRect(-2, -10, 4, 12);
  ctx.fillStyle = "#3b9a55";
  ctx.beginPath();
  ctx.ellipse(-5, -8, 7, 4, -0.5, 0, Math.PI * 2);
  ctx.ellipse(5, -12, 7, 4, 0.5, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function drawAnimal(a, emoji, size) {
  ctx.save();
  ctx.font = `${size}px serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(emoji, a.x, a.y);
  ctx.restore();
}

function draw() {
  drawBackground();

  plants.forEach(drawPlant);
  rabbits.forEach(a => drawAnimal(a, "🐇", 23));
  foxes.forEach(a => drawAnimal(a, "🦊", 25));
  butterflies.forEach(a => drawAnimal(a, "🦋", 17));

  // Weather effects.
  if (weather === "rain") {
    ctx.strokeStyle = "#d7f0ff";
    ctx.lineWidth = 2;
    for (let i = 0; i < 45; i++) {
      const x = (i * 83 + day * 19) % W;
      const y = (i * 47 + day * 29) % H;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x - 5, y + 12);
      ctx.stroke();
    }
  }

  if (weather === "drought") {
    ctx.fillStyle = "rgba(255, 170, 65, 0.12)";
    ctx.fillRect(0, 0, W, H);
  }

  if (gameOver) {
    ctx.fillStyle = "rgba(12, 28, 20, 0.5)";
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 34px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(day >= 100 ? "ISLAND SAVED!" : "ECOSYSTEM COLLAPSED", W / 2, H / 2);
  }
}

function moveCreatures(list, amount = 1) {
  list.forEach(a => {
    a.phase += 0.03 * amount;
    a.x += a.dx * amount + Math.sin(a.phase) * 0.25;
    a.y += a.dy * amount + Math.cos(a.phase) * 0.25;

    // Keep animals within the island.
    const dx = a.x - 450;
    const dy = a.y - 280;
    const distance = Math.sqrt(dx * dx / (350 * 350) + dy * dy / (205 * 205));

    if (distance > 0.95) {
      a.dx *= -1;
      a.dy *= -1;
    }

    a.dx += random(-0.025, 0.025);
    a.dy += random(-0.025, 0.025);
    a.dx = Math.max(-1, Math.min(1, a.dx));
    a.dy = Math.max(-1, Math.min(1, a.dy));
  });
}

function animate() {
  if (running && !gameOver) {
    timer++;
    if (timer >= 180 / speed) {
      timer = 0;
      simulateDay();
    }

    moveCreatures(rabbits, speed);
    moveCreatures(foxes, speed);
    moveCreatures(butterflies, speed * 1.5);

    clouds.forEach(cloud => {
      cloud.x += cloud.speed * speed;
      if (cloud.x > W + 80) cloud.x = -100;
    });
  }

  draw();
  requestAnimationFrame(animate);
}

createWorld();
animate();
