
const canvas = document.getElementById("world");
const ctx = canvas.getContext("2d");

const $ = id => document.getElementById(id);

const W = 900;
const H = 600;

let world;
let selectedTool = "select";
let paused = false;
let speed = 1;
let lastTick = 0;
let notificationTimer;
let particles = [];

const notes = [
  "A new ecosystem begins with a single seed. Give it time, light and water.",
  "Flowers attract pollinators. Try planting several close together.",
  "Trees provide shelter for birds and help create a balanced habitat.",
  "Mushrooms prefer damp places. They are a sign of a thriving forest floor.",
  "A pond brings water into your world and can support a richer ecosystem.",
  "Too much sunlight can dry out the soil. Balance is everything.",
  "Your ecosystem is becoming more diverse. Keep experimenting!",
  "Rain restores moisture. Watch how your plants respond."
];

const plantTypes = {
  grass: { emoji: "🌱", growth: 0.9, water: 0.8 },
  flower: { emoji: "🌼", growth: 0.7, water: 1.0 },
  tree: { emoji: "🌳", growth: 0.35, water: 1.1 },
  mushroom: { emoji: "🍄", growth: 0.55, water: 0.5 },
  pond: { emoji: "💧", growth: 0, water: 0 }
};

function newWorld() {
  return {
    day: 1,
    sunlight: 70,
    moisture: 65,
    weather: "clear",
    objects: [],
    creatures: [],
    discoveries: [],
    health: 100,
    time: 0
  };
}

function loadWorld() {
  try {
    const saved = JSON.parse(localStorage.getItem("terrarium-world"));
    if (saved && Array.isArray(saved.objects)) {
      return { ...newWorld(), ...saved };
    }
  } catch (error) {
    console.warn("Could not load saved world:", error);
  }
  return newWorld();
}

world = loadWorld();

function saveWorld() {
  localStorage.setItem("terrarium-world", JSON.stringify(world));
  document.querySelector(".save-status").textContent = "● WORLD SAVED";
}

function notify(message) {
  const box = $("notification");
  box.textContent = message;
  box.classList.add("show");
  clearTimeout(notificationTimer);
  notificationTimer = setTimeout(() => box.classList.remove("show"), 2200);
}

function resizeCanvas() {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(rect.width * dpr);
  canvas.height = Math.round(rect.height * dpr);
  ctx.setTransform(canvas.width / W, 0, 0, canvas.height / H, 0, 0);
  draw();
}

function random(min, max) {
  return Math.random() * (max - min) + min;
}

function drawBackground() {
  const sky = ctx.createLinearGradient(0, 0, 0, H);
  sky.addColorStop(0, world.weather === "cloudy" ? "#8b9e9b" : "#9dc9c1");
  sky.addColorStop(1, "#d0dfb3");

  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, W, H);

  // Sun
  if (world.weather === "clear") {
    ctx.fillStyle = "#f9e7a2";
    ctx.beginPath();
    ctx.arc(740, 100, 43, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#fff1ba55";
    ctx.beginPath();
    ctx.arc(740, 100, 60, 0, Math.PI * 2);
    ctx.fill();
  }

  // Clouds
  if (world.weather !== "clear") {
    for (let i = 0; i < 5; i++) {
      const x = (i * 215 + 40) % 1000;
      ctx.fillStyle = world.weather === "rain" ? "#a3b1ae" : "#d9e2d6";
      ctx.beginPath();
      ctx.arc(x, 85, 28, 0, Math.PI * 2);
      ctx.arc(x + 30, 70, 35, 0, Math.PI * 2);
      ctx.arc(x + 65, 88, 25, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Distant hills
  ctx.fillStyle = "#83ad84";
  ctx.beginPath();
  ctx.moveTo(0, 350);
  ctx.quadraticCurveTo(190, 205, 390, 355);
  ctx.quadraticCurveTo(620, 190, 900, 340);
  ctx.lineTo(900, 600);
  ctx.lineTo(0, 600);
  ctx.fill();

  // Main ground
  ctx.fillStyle = "#557e4d";
  ctx.beginPath();
  ctx.moveTo(0, 385);
  ctx.quadraticCurveTo(220, 330, 450, 400);
  ctx.quadraticCurveTo(700, 340, 900, 390);
  ctx.lineTo(900, 600);
  ctx.lineTo(0, 600);
  ctx.fill();

  // Grass texture
  for (let i = 0; i < 170; i++) {
    const x = (i * 67) % W;
    const y = 390 + ((i * 47) % 200);
    ctx.strokeStyle = i % 2 ? "#8db66b66" : "#294f3966";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + random(-5, 5), y - random(3, 10));
    ctx.stroke();
  }
}

function drawObject(obj) {
  const type = obj.type;
  const size = 0.5 + obj.growth * 0.5;

  ctx.save();
  ctx.translate(obj.x, obj.y);
  ctx.globalAlpha = Math.max(0.15, obj.health);

  if (type === "pond") {
    ctx.fillStyle = "#357d92";
    ctx.beginPath();
    ctx.ellipse(0, 0, 42, 23, -0.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#9de0db";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.ellipse(-5, -5, 20, 7, -0.2, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
    return;
  }

  if (type === "tree") {
    ctx.fillStyle = "#76533a";
    ctx.fillRect(-5 * size, -35 * size, 10 * size, 37 * size);
    ctx.fillStyle = "#285b38";
    ctx.beginPath();
    ctx.arc(0, -48 * size, 29 * size, 0, Math.PI * 2);
    ctx.arc(-17 * size, -36 * size, 21 * size, 0, Math.PI * 2);
    ctx.arc(17 * size, -36 * size, 21 * size, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#568b4c";
    ctx.beginPath();
    ctx.arc(-8 * size, -55 * size, 11 * size, 0, Math.PI * 2);
    ctx.fill();
  } else if (type === "grass") {
    ctx.strokeStyle = "#b1d77b";
    ctx.lineWidth = 4 * size;
    for (let i = -2; i <= 2; i++) {
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.quadraticCurveTo(i * 9, -15 * size, i * 12, -27 * size);
      ctx.stroke();
    }
  } else if (type === "flower") {
    ctx.strokeStyle = "#4a8c45";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, -28 * size);
    ctx.stroke();
    for (let i = 0; i < 6; i++) {
      const a = i * Math.PI / 3;
      ctx.fillStyle = "#f4c6d3";
      ctx.beginPath();
      ctx.arc(Math.cos(a) * 8 * size, -28 * size + Math.sin(a) * 8 * size, 6 * size, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.fillStyle = "#f6d76a";
    ctx.beginPath();
    ctx.arc(0, -28 * size, 5 * size, 0, Math.PI * 2);
    ctx.fill();
  } else if (type === "mushroom") {
    ctx.fillStyle = "#e9d5b4";
    ctx.fillRect(-4 * size, -18 * size, 8 * size, 18 * size);
    ctx.fillStyle = "#b95646";
    ctx.beginPath();
    ctx.arc(0, -18 * size, 13 * size, Math.PI, 0);
    ctx.fill();
    ctx.fillStyle = "#fff1dc";
    ctx.beginPath();
    ctx.arc(-5 * size, -21 * size, 2 * size, 0, Math.PI * 2);
    ctx.arc(5 * size, -22 * size, 2 * size, 0, Math.PI * 2);
    ctx.fill();
  }

  // Growth indicator
  if (obj.growth < 1) {
    ctx.fillStyle = "#ffffffaa";
    ctx.beginPath();
    ctx.arc(0, 10, 3, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.restore();
}

function drawCreature(creature) {
  const emojis = {
    butterfly: "🦋",
    bee: "🐝",
    bird: "🐦"
  };

  ctx.save();
  ctx.font = "23px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(emojis[creature.type], creature.x, creature.y);
  ctx.restore();
}

function draw() {
  ctx.clearRect(0, 0, W, H);
  drawBackground();

  world.objects
    .slice()
    .sort((a, b) => a.y - b.y)
    .forEach(drawObject);

  world.creatures.forEach(drawCreature);

  // Rain particles
  if (world.weather === "rain") {
    ctx.strokeStyle = "#d9f0ff99";
    ctx.lineWidth = 1.5;
    for (let i = 0; i < 50; i++) {
      const x = (i * 83 + world.time * 35) % W;
      const y = (i * 37 + world.time * 75) % H;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x - 5, y + 12);
      ctx.stroke();
    }
  }

  // Ground border
  ctx.strokeStyle = "#e4f2bd55";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, 389);
  ctx.quadraticCurveTo(220, 330, 450, 400);
  ctx.quadraticCurveTo(700, 340, 900, 390);
  ctx.stroke();
}

function addObject(type, x, y) {
  if (world.objects.length >= 120) {
    notify("Your world is full! Remove some plants first.");
    return;
  }

  const near = world.objects.some(obj =>
    Math.hypot(obj.x - x, obj.y - y) < (type === "tree" ? 48 : 23)
  );

  if (near) {
    notify("That spot is already occupied. Try another!");
    return;
  }

  if (type === "water") {
    world.moisture = Math.min(100, world.moisture + 16);
    notify("💧 Fresh water added to the soil!");
    updateUI();
    saveWorld();
    return;
  }

  if (!plantTypes[type]) return;

  world.objects.push({
    type,
    x,
    y,
    growth: type === "pond" ? 1 : 0.1,
    health: 1
  });

  if (type === "pond") {
    world.moisture = Math.min(100, world.moisture + 12);
  }

  notify(`${plantTypes[type].emoji} ${type[0].toUpperCase() + type.slice(1)} planted!`);
  updateUI();
  saveWorld();
}

canvas.addEventListener("click", event => {
  const rect = canvas.getBoundingClientRect();
  const x = (event.clientX - rect.left) / rect.width * W;
  const y = (event.clientY - rect.top) / rect.height * H;

  if (y < 375) {
    notify("Choose a spot on the ground to plant!");
    return;
  }

  if (selectedTool === "select") {
    const nearby = world.objects.find(obj =>
      Math.hypot(obj.x - x, obj.y - y) < 45
    );
    if (nearby) {
      notify(`${nearby.type.toUpperCase()} · Growth ${Math.round(nearby.growth * 100)}%`);
    } else {
      notify("Choose a tool to add something to your world.");
    }
    return;
  }

  addObject(selectedTool, x, y);
});

document.querySelectorAll(".tool").forEach(button => {
  button.addEventListener("click", () => {
    selectedTool = button.dataset.tool;
    document.querySelectorAll(".tool").forEach(b => b.classList.remove("active"));
    button.classList.add("active");
  });
});

$("sun").addEventListener("input", event => {
  world.sunlight = Number(event.target.value);
  updateUI();
  saveWorld();
});

$("moisture").addEventListener("input", event => {
  world.moisture = Number(event.target.value);
  updateUI();
  saveWorld();
});

document.querySelectorAll("[data-weather]").forEach(button => {
  button.addEventListener("click", () => {
    world.weather = button.dataset.weather;
    if (world.weather === "rain") {
      world.moisture = Math.min(100, world.moisture + 15);
      notify("🌧 Rain is falling! Soil moisture restored.");
    } else {
      notify(`Weather changed to ${world.weather}.`);
    }
    updateUI();
    saveWorld();
  });
});

$("pause").addEventListener("click", () => {
  paused = !paused;
  $("pause").textContent = paused ? "▶ Resume" : "Ⅱ Pause";
  notify(paused ? "Time paused." : "Your world is alive again.");
});

document.querySelectorAll(".speed").forEach(button => {
  button.addEventListener("click", () => {
    speed = Number(button.dataset.speed);
    document.querySelectorAll(".speed").forEach(b => b.classList.remove("active"));
    button.classList.add("active");
    $("speed-label").textContent = speed + "× SPEED";
  });
});

function spawnCreature() {
  const flowers = world.objects.filter(o => o.type === "flower" && o.growth > 0.5).length;
  const trees = world.objects.filter(o => o.type === "tree" && o.growth > 0.5).length;

  if (flowers > 0 && Math.random() < 0.35) {
    const type = Math.random() < 0.55 ? "butterfly" : "bee";
    world.creatures.push({
      type,
      x: random(100, 800),
      y: random(310, 390),
      phase: random(0, 6)
    });
    return;
  }

  if (trees >= 2 && Math.random() < 0.25) {
    world.creatures.push({
      type: "bird",
      x: random(100, 800),
      y: random(160, 300),
      phase: random(0, 6)
    });
  }
}

function updateCreatures() {
  world.creatures.forEach(creature => {
    creature.phase += 0.04;
    creature.x += Math.sin(creature.phase) * 1.2;
    creature.y += Math.cos(creature.phase * 0.8) * 0.5;
  });

  world.creatures = world.creatures.filter(() =>
    Math.random() > 0.002
  );
}

function updateEcosystem() {
  world.time += 1;

  if (world.weather === "rain") {
    world.moisture = Math.min(100, world.moisture + 0.8);
  } else {
    world.moisture = Math.max(0, world.moisture - 0.12);
  }

  world.objects.forEach(obj => {
    if (obj.type === "pond") return;

    const sunlightFactor = Math.max(0, 1 - Math.abs(world.sunlight - 65) / 90);
    const waterFactor = Math.max(0, 1 - Math.abs(world.moisture - 65) / 90);

    const growthRate = plantTypes[obj.type].growth * 0.0008;
    const conditions = sunlightFactor * waterFactor;

    obj.growth = Math.min(1, obj.growth + growthRate * conditions);

    if (conditions > 0.25) {
      obj.health = Math.min(1, obj.health + 0.0002);
    } else {
      obj.health = Math.max(0.15, obj.health - 0.0004);
    }
  });

  // Occasionally grow new grass near existing grass.
  if (Math.random() < 0.006) {
    const grass = world.objects.filter(o => o.type === "grass" && o.growth > 0.6);
    if (grass.length && world.objects.length < 100) {
      const parent = grass[Math.floor(Math.random() * grass.length)];
      const x = parent.x + random(-55, 55);
      const y = parent.y + random(-25, 25);
      if (x > 25 && x < 875 && y > 380 && y < 575 &&
          !world.objects.some(o => Math.hypot(o.x - x, o.y - y) < 22)) {
        world.objects.push({ type: "grass", x, y, growth: 0.1, health: 1 });
      }
    }
  }

  if (Math.random() < 0.02) spawnCreature();

  updateCreatures();

  if (world.time % 100 === 0) {
    world.day++;
    if (!world.discoveries.includes(world.day)) {
      world.discoveries.push(world.day);
    }
    notify(`🌅 A new day begins! Day ${world.day}`);
    saveWorld();
  }

  // Ecosystem health
  const healthyPlants = world.objects.filter(o => o.type !== "pond" && o.health > 0.5).length;
  const plantVariety = new Set(world.objects.map(o => o.type)).size;
  const conditionsScore = 100 - Math.abs(world.sunlight - 65) * 0.5 - Math.abs(world.moisture - 65) * 0.5;
  const biodiversityBonus = Math.min(25, plantVariety * 5 + world.creatures.length * 2);

  world.health = Math.round(Math.max(0, Math.min(100,
    conditionsScore * 0.7 + Math.min(healthyPlants * 3, 30) + biodiversityBonus
  )));
}

function updateUI() {
  $("day").textContent = `DAY ${String(world.day).padStart(2, "0")}`;
  $("sun").value = world.sunlight;
  $("moisture").value = world.moisture;
  $("sun-value").textContent = world.sunlight + "%";
  $("moisture-value").textContent = Math.round(world.moisture) + "%";

  $("weather-label").textContent = {
    clear: "☀ CLEAR SKIES",
    rain: "🌧 RAINFALL",
    cloudy: "☁ CLOUDY"
  }[world.weather];

  $("time-label").textContent = ["MORNING", "AFTERNOON", "EVENING", "NIGHT"][Math.floor(world.time / 25) % 4];

  const objects = world.objects;
  const count = type => objects.filter(o => o.type === type).length;

  $("plants").textContent = count("grass") + count("flower");
  $("trees").textContent = count("tree");
  $("mushrooms").textContent = count("mushroom");
  $("butterflies").textContent = world.creatures.filter(c => c.type === "butterfly").length;
  $("bees").textContent = world.creatures.filter(c => c.type === "bee").length;
  $("birds").textContent = world.creatures.filter(c => c.type === "bird").length;

  $("health").textContent = world.health;
  $("health-bar").style.width = world.health + "%";

  $("health-message").textContent =
    world.health > 80 ? "Your ecosystem is thriving." :
    world.health > 55 ? "Your ecosystem is finding its balance." :
    world.health > 30 ? "Your ecosystem needs some care." :
    "Conditions are difficult. Adjust sunlight and water.";

  $("age").textContent = `${world.day - 1} days`;

  $("field-note").textContent =
    notes[Math.min(notes.length - 1, Math.floor(world.day / 2))];

  $("weather-label").textContent = {
    clear: "☀ CLEAR SKIES",
    rain: "🌧 RAINFALL",
    cloudy: "☁ CLOUDY"
  }[world.weather];
}

function loop(timestamp) {
  if (!lastTick) lastTick = timestamp;
  const elapsed = timestamp - lastTick;
  lastTick = timestamp;

  if (!paused) {
    const ticks = Math.min(5, Math.floor(elapsed / 100) || 1);
    for (let i = 0; i < ticks * speed; i++) {
      updateEcosystem();
    }
    updateUI();
  }

  draw();
  requestAnimationFrame(loop);
}

$("reset").addEventListener("click", () => {
  if (!confirm("Start over? Your current ecosystem will be erased.")) return;
  world = newWorld();
  paused = false;
  speed = 1;
  $("pause").textContent = "Ⅱ Pause";
  document.querySelectorAll(".speed").forEach(b => {
    b.classList.toggle("active", b.dataset.speed === "1");
  });
  $("speed-label").textContent = "1× SPEED";
  saveWorld();
  updateUI();
  notify("A fresh new world awaits you.");
});

updateUI();
resizeCanvas();
window.addEventListener("resize", resizeCanvas);
requestAnimationFrame(loop);
