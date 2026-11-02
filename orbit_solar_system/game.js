
"use strict";

// ============================================
// ORBIT — SOLAR SYSTEM SIMULATOR
// ============================================

const canvas = document.getElementById("spaceCanvas");
const ctx = canvas.getContext("2d");

const $ = (id) => document.getElementById(id);

// ============================================
// SIMULATION STATE
// ============================================

let running = true;
let timeSpeed = 1;
let simulationDays = 1;
let selectedId = 2;
let nextId = 5;

let width = 0;
let height = 0;
let centerX = 0;
let centerY = 0;
let pixelRatio = 1;

// ============================================
// ORIGINAL PLANETS
// ============================================

function createOriginalPlanets() {
  return [
    {
      id: 1,
      name: "Mercury",
      size: 5,
      orbit: 65,
      speed: 2.4,
      angle: 0.5,
      color: "#b7a38d",
      description: "Small rocky planet"
    },
    {
      id: 2,
      name: "Earth",
      size: 10,
      orbit: 125,
      speed: 1,
      angle: 2.1,
      color: "#5e9eff",
      description: "Terrestrial planet"
    },
    {
      id: 3,
      name: "Mars",
      size: 8,
      orbit: 175,
      speed: 0.65,
      angle: 3.8,
      color: "#e5a16b",
      description: "Red rocky planet"
    },
    {
      id: 4,
      name: "Jupiter",
      size: 19,
      orbit: 240,
      speed: 0.35,
      angle: 5.2,
      color: "#e8d58b",
      description: "Gas giant"
    }
  ];
}

let planets = createOriginalPlanets();

// ============================================
// BACKGROUND STARS
// ============================================

let stars = [];

function createStars() {
  stars = [];

  for (let i = 0; i < 120; i++) {
    stars.push({
      x: Math.random(),
      y: Math.random(),
      radius: Math.random() * 1.5 + 0.3,
      alpha: Math.random() * 0.6 + 0.2,
      twinkle: Math.random() * 0.02 + 0.005
    });
  }
}

createStars();

// ============================================
// CANVAS SIZE
// ============================================

function resizeCanvas() {
  const rect = canvas.getBoundingClientRect();

  pixelRatio = Math.min(window.devicePixelRatio || 1, 2);

  width = rect.width;
  height = rect.height;

  canvas.width = Math.round(width * pixelRatio);
  canvas.height = Math.round(height * pixelRatio);

  ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);

  centerX = width / 2;
  centerY = height / 2;
}

window.addEventListener("resize", resizeCanvas);

resizeCanvas();

// ============================================
// DRAW BACKGROUND
// ============================================

function drawBackground() {
  ctx.clearRect(0, 0, width, height);

  stars.forEach((star) => {
    star.alpha += star.twinkle;

    if (star.alpha > 0.85 || star.alpha < 0.15) {
      star.twinkle *= -1;
    }

    ctx.beginPath();
    ctx.arc(
      star.x * width,
      star.y * height,
      star.radius,
      0,
      Math.PI * 2
    );

    ctx.fillStyle = `rgba(210, 225, 255, ${star.alpha})`;
    ctx.fill();
  });
}

// ============================================
// DRAW CENTRAL STAR
// ============================================

function drawSun() {
  const glow = ctx.createRadialGradient(
    centerX,
    centerY,
    2,
    centerX,
    centerY,
    48
  );

  glow.addColorStop(0, "#fff8c9");
  glow.addColorStop(0.2, "#ffd76c");
  glow.addColorStop(0.55, "#ff9e43");
  glow.addColorStop(1, "rgba(255, 130, 50, 0)");

  ctx.beginPath();
  ctx.arc(centerX, centerY, 48, 0, Math.PI * 2);
  ctx.fillStyle = glow;
  ctx.fill();

  ctx.beginPath();
  ctx.arc(centerX, centerY, 12, 0, Math.PI * 2);
  ctx.fillStyle = "#fff2b0";
  ctx.shadowColor = "#ffb84d";
  ctx.shadowBlur = 25;
  ctx.fill();

  ctx.shadowBlur = 0;
}

// ============================================
// DRAW ORBIT PATHS
// ============================================

function drawOrbit(planet) {
  ctx.beginPath();

  ctx.ellipse(
    centerX,
    centerY,
    planet.orbit,
    planet.orbit * 0.62,
    0,
    0,
    Math.PI * 2
  );

  ctx.strokeStyle =
    planet.id === selectedId
      ? "rgba(112, 169, 255, 0.45)"
      : "rgba(135, 163, 195, 0.17)";

  ctx.lineWidth = planet.id === selectedId ? 1.4 : 1;
  ctx.stroke();
}

// ============================================
// PLANET POSITION
// ============================================

function getPlanetPosition(planet) {
  return {
    x: centerX + Math.cos(planet.angle) * planet.orbit,
    y: centerY + Math.sin(planet.angle) * planet.orbit * 0.62
  };
}

// ============================================
// DRAW PLANETS
// ============================================

function drawPlanet(planet) {
  const position = getPlanetPosition(planet);

  const glow = ctx.createRadialGradient(
    position.x,
    position.y,
    1,
    position.x,
    position.y,
    planet.size * 3
  );

  glow.addColorStop(0, planet.color + "66");
  glow.addColorStop(1, planet.color + "00");

  ctx.beginPath();
  ctx.arc(
    position.x,
    position.y,
    planet.size * 3,
    0,
    Math.PI * 2
  );
  ctx.fillStyle = glow;
  ctx.fill();

  ctx.beginPath();
  ctx.arc(
    position.x,
    position.y,
    planet.size,
    0,
    Math.PI * 2
  );

  ctx.fillStyle = planet.color;
  ctx.shadowColor = planet.color;
  ctx.shadowBlur = 14;
  ctx.fill();
  ctx.shadowBlur = 0;

  // Small highlight
  ctx.beginPath();
  ctx.arc(
    position.x - planet.size * 0.3,
    position.y - planet.size * 0.3,
    Math.max(1, planet.size * 0.22),
    0,
    Math.PI * 2
  );

  ctx.fillStyle = "#ffffff88";
  ctx.fill();

  // Planet label
  ctx.fillStyle = "#c5d4e8";
  ctx.font = "10px DM Mono";
  ctx.textAlign = "center";
  ctx.fillText(
    planet.name,
    position.x,
    position.y + planet.size + 15
  );

  // Selection ring
  if (planet.id === selectedId) {
    ctx.beginPath();
    ctx.arc(
      position.x,
      position.y,
      planet.size + 6,
      0,
      Math.PI * 2
    );

    ctx.strokeStyle = "#71d7e8";
    ctx.lineWidth = 1;
    ctx.stroke();
  }
}

// ============================================
// UPDATE PLANET MOTION
// ============================================

function updatePlanets() {
  if (!running) return;

  planets.forEach((planet) => {
    planet.angle += planet.speed * 0.003 * timeSpeed;
  });

  simulationDays += 0.08 * timeSpeed;
}

// ============================================
// RENDER SIMULATION
// ============================================

function render() {
  drawBackground();

  // Draw orbits first
  planets.forEach(drawOrbit);

  drawSun();

  // Draw planets
  planets.forEach(drawPlanet);

  updatePlanets();

  requestAnimationFrame(render);
}

// ============================================
// SELECT PLANET
// ============================================

function selectPlanet(id) {
  const planet = planets.find((item) => item.id === id);

  if (!planet) return;

  selectedId = id;

  $("selectedName").textContent = planet.name;
  $("selectedDescription").textContent = planet.description;

  $("sizeRange").value = planet.size;
  $("orbitRange").value = planet.orbit;
  $("planetSpeedRange").value = planet.speed;
  $("colorSelect").value = planet.color;

  $("sizeValue").textContent = planet.size;
  $("orbitValue").textContent = planet.orbit;
  $("planetSpeedValue").textContent = `${planet.speed.toFixed(1)}×`;

  $("statSelected").textContent = planet.name.toUpperCase();

  updatePlanetList();
}

// ============================================
// PLANET LIST
// ============================================

function updatePlanetList() {
  const list = $("planetList");

  list.innerHTML = "";

  planets.forEach((planet) => {
    const button = document.createElement("button");

    button.className =
      "planet-item" +
      (planet.id === selectedId ? " selected" : "");

    const dot = document.createElement("span");
    dot.className = "planet-dot";
    dot.style.background = planet.color;
    dot.style.color = planet.color;

    const name = document.createElement("span");
    name.textContent = planet.name;

    const size = document.createElement("small");
    size.textContent = `${planet.size} PX`;

    button.append(dot, name, size);

    button.addEventListener("click", () => {
      selectPlanet(planet.id);
    });

    list.appendChild(button);
  });

  $("listCount").textContent =
    String(planets.length).padStart(2, "0");

  $("planetCount").textContent =
    `${planets.length + 1} OBJECTS`;

  $("statBodies").textContent =
    String(planets.length + 1).padStart(2, "0");
}

// ============================================
// UPDATE SELECTED PLANET
// ============================================

function updateSelectedPlanet(property, value) {
  const planet = planets.find((item) => item.id === selectedId);

  if (!planet) return;

  planet[property] = value;

  if (property === "size") {
    $("sizeValue").textContent = value;
  }

  if (property === "orbit") {
    $("orbitValue").textContent = value;
  }

  if (property === "speed") {
    $("planetSpeedValue").textContent = `${value.toFixed(1)}×`;
  }

  updatePlanetList();
}

// ============================================
// CANVAS PLANET SELECTION
// ============================================

canvas.addEventListener("click", (event) => {
  const rect = canvas.getBoundingClientRect();

  const mouseX = event.clientX - rect.left;
  const mouseY = event.clientY - rect.top;

  for (const planet of planets) {
    const position = getPlanetPosition(planet);

    const distance = Math.hypot(
      mouseX - position.x,
      mouseY - position.y
    );

    if (distance < planet.size + 12) {
      selectPlanet(planet.id);
      return;
    }
  }
});

// ============================================
// CUSTOMIZATION CONTROLS
// ============================================

$("sizeRange").addEventListener("input", (event) => {
  updateSelectedPlanet("size", Number(event.target.value));
});

$("orbitRange").addEventListener("input", (event) => {
  updateSelectedPlanet("orbit", Number(event.target.value));
});

$("planetSpeedRange").addEventListener("input", (event) => {
  updateSelectedPlanet("speed", Number(event.target.value));
});

$("colorSelect").addEventListener("change", (event) => {
  updateSelectedPlanet("color", event.target.value);
});

// ============================================
// CREATE NEW PLANET
// ============================================

$("addPlanetButton").addEventListener("click", () => {
  if (planets.length >= 10) {
    alert("Maximum of 10 planets reached!");
    return;
  }

  const colors = [
    "#5e9eff",
    "#e5a16b",
    "#b18aff",
    "#8bd6a0",
    "#e8d58b",
    "#ef8298"
  ];

  const newPlanet = {
    id: nextId,
    name: `Planet ${nextId - 4}`,
    size: 9,
    orbit: 75 + planets.length * 24,
    speed: 0.8,
    angle: Math.random() * Math.PI * 2,
    color: colors[Math.floor(Math.random() * colors.length)],
    description: "Custom celestial body"
  };

  planets.push(newPlanet);
  nextId++;

  selectPlanet(newPlanet.id);
  updatePlanetList();
});

// ============================================
// PAUSE / RESUME
// ============================================

$("playButton").addEventListener("click", () => {
  running = !running;

  $("playIcon").textContent = running ? "Ⅱ" : "▶";
  $("playText").textContent = running ? "PAUSE" : "RESUME";

  $("simulationStatus").textContent =
    running ? "RUNNING" : "PAUSED";

  $("simulationStatus").style.color =
    running ? "#82d6a3" : "#e8d58b";
});

// ============================================
// SIMULATION SPEED
// ============================================

$("speedRange").addEventListener("input", (event) => {
  timeSpeed = Number(event.target.value);

  $("speedValue").textContent = `${timeSpeed.toFixed(1)}×`;
  $("statSpeed").textContent = `${timeSpeed.toFixed(1)}×`;
});

// ============================================
// RESET SYSTEM
// ============================================

$("resetButton").addEventListener("click", () => {
  const confirmed = confirm(
    "Reset your solar system to its original state?"
  );

  if (!confirmed) return;

  planets = createOriginalPlanets();

  selectedId = 2;
  nextId = 5;
  timeSpeed = 1;
  simulationDays = 1;
  running = true;

  $("speedRange").value = 1;
  $("speedValue").textContent = "1.0×";
  $("statSpeed").textContent = "1.0×";

  $("playIcon").textContent = "Ⅱ";
  $("playText").textContent = "PAUSE";
  $("simulationStatus").textContent = "RUNNING";
  $("simulationStatus").style.color = "#82d6a3";

  selectPlanet(selectedId);
  updatePlanetList();
});

// ============================================
// SIMULATION CLOCK
// ============================================

function updateSimulationClock() {
  $("simulationTime").textContent =
    `DAY ${String(Math.floor(simulationDays)).padStart(3, "0")}`;

  requestAnimationFrame(updateSimulationClock);
}

// ============================================
// INITIALIZE
// ============================================

function initialize() {
  resizeCanvas();

  selectPlanet(selectedId);
  updatePlanetList();

  render();
  updateSimulationClock();

  console.log("ORBIT simulation initialized.");
  console.log("Planetary engine online.");
}

initialize();
