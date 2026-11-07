
const eras = [
  { min: 1900, max: 1949, name: "THE EARLY CENTURY", description: "A world of industrial revolutions, steam engines and changing empires." },
  { min: 1950, max: 1968, name: "THE SPACE RACE", description: "Humanity is reaching beyond Earth. The race to the stars has begun." },
  { min: 1969, max: 1989, name: "THE MOON ERA", description: "One giant leap has changed the future of human exploration." },
  { min: 1990, max: 2009, name: "THE DIGITAL REVOLUTION", description: "The internet connects the world. A new age of information begins." },
  { min: 2010, max: 2039, name: "THE PRESENT AGE", description: "Artificial intelligence, global networks and rapid technological change." },
  { min: 2040, max: 2099, name: "THE NEON CENTURY", description: "Cities have transformed. Autonomous systems shape everyday life." },
  { min: 2100, max: 2149, name: "THE EXPANSION", description: "Human settlements reach further into the solar system." },
  { min: 2150, max: 2200, name: "THE NEW FRONTIER", description: "Humanity enters an era that once existed only in imagination." }
];

const discoveries = [
  { year: 1920, title: "The Jazz Age", detail: "A cultural revolution echoes through the cities." },
  { year: 1945, title: "A Changing World", detail: "A new international order begins to emerge." },
  { year: 1969, title: "One Giant Leap", detail: "Humans reach the lunar surface." },
  { year: 1984, title: "The Digital Spark", detail: "Personal computing enters a new chapter." },
  { year: 2000, title: "The Millennium", detail: "A new millennium begins." },
  { year: 2026, title: "The Present", detail: "Your own era. The starting point of the experiment." },
  { year: 2089, title: "Neon Century", detail: "A transformed city rises around the temporal network." },
  { year: 2150, title: "New Frontier", detail: "A distant future opens new possibilities." }
];

const missions = [
  {
    title: "The First Jump",
    description: "Travel to a different year to begin your research."
  },
  {
    title: "Historical Observer",
    description: "Visit a year before 2000 and document the past."
  },
  {
    title: "Future Architect",
    description: "Explore a year beyond 2100."
  },
  {
    title: "Timeline Explorer",
    description: "Discover four unique temporal coordinates."
  },
  {
    title: "Chronos Master",
    description: "Collect all eight discoveries."
  }
];

const slider = document.getElementById("yearSlider");
const yearDisplay = document.getElementById("yearDisplay");
const selectedYear = document.getElementById("selectedYear");
const eraName = document.getElementById("eraName");
const eraDescription = document.getElementById("eraDescription");
const jumpBtn = document.getElementById("jumpBtn");
const logElement = document.getElementById("log");
const anomaly = document.getElementById("anomaly");
const anomalyText = document.getElementById("anomalyText");

const saved = JSON.parse(localStorage.getItem("chronosSave") || "{}");

let currentYear = Number(saved.currentYear) || 2026;
let targetYear = currentYear;
let stability = Number.isFinite(saved.stability) ? saved.stability : 100;
let integrity = Number.isFinite(saved.integrity) ? saved.integrity : 100;
let found = Array.isArray(saved.found) ? saved.found : [];
let history = Array.isArray(saved.history) ? saved.history : [];
let anomalyActive = false;
let jumpCount = Number(saved.jumpCount) || 0;

function getEra(year) {
  return eras.find(era => year >= era.min && year <= era.max);
}

function save() {
  localStorage.setItem("chronosSave", JSON.stringify({
    currentYear,
    stability,
    integrity,
    found,
    history,
    jumpCount
  }));
}

function updateMeters() {
  stability = Math.max(0, Math.min(100, stability));
  integrity = Math.max(0, Math.min(100, integrity));

  document.getElementById("stabilityText").textContent = `${Math.round(stability)}%`;
  document.getElementById("integrityText").textContent = `${Math.round(integrity)}%`;

  document.getElementById("stabilityBar").style.width = `${stability}%`;
  document.getElementById("integrityBar").style.width = `${integrity}%`;

  document.getElementById("discoveryCount").textContent = `${found.length} / 8`;

  document.getElementById("stabilityBar").style.background =
    stability < 35 ? "#ff7373" : "#62e5d0";

  document.getElementById("integrityBar").style.background =
    integrity < 35 ? "#ff7373" : "#62e5d0";
}

function addLog(message, year = currentYear) {
  history.unshift({ message, year });
  history = history.slice(0, 12);
  renderLog();
}

function renderLog() {
  if (history.length === 0) {
    logElement.innerHTML = '<p class="muted">No temporal activity recorded.</p>';
    return;
  }

  logElement.innerHTML = "";

  history.forEach(item => {
    const entry = document.createElement("div");
    entry.className = "log-entry";

    const time = document.createElement("small");
    time.textContent = `YEAR ${item.year}`;

    const message = document.createElement("span");
    message.textContent = item.message;

    entry.append(time, message);
    logElement.appendChild(entry);
  });
}

function renderTarget(year) {
  targetYear = year;
  const era = getEra(year);

  selectedYear.textContent = year;
  eraName.textContent = era.name;
  eraDescription.textContent = era.description;

  document.querySelectorAll(".destination-grid button").forEach(button => {
    button.classList.toggle("active", Number(button.dataset.year) === year);
  });

  updateMission();
}

function updateMission() {
  let mission;

  if (jumpCount === 0) {
    mission = missions[0];
  } else if (currentYear < 2000) {
    mission = missions[2];
  } else if (currentYear > 2100) {
    mission = missions[3];
  } else if (found.length === 8) {
    mission = missions[4];
  } else if (jumpCount >= 3) {
    mission = missions[3];
  } else {
    mission = missions[1];
  }

  document.getElementById("missionTitle").textContent = mission.title;
  document.getElementById("missionDescription").textContent = mission.description;
}

function findDiscovery(year) {
  const discovery = discoveries.find(item =>
    item.year === year && !found.includes(item.year)
  );

  if (discovery) {
    found.push(discovery.year);
    addLog(`DISCOVERY: ${discovery.title}`, year);
    return true;
  }

  return false;
}

function maybeCreateAnomaly() {
  if (anomalyActive || Math.random() > 0.45) return;

  anomalyActive = true;

  const events = [
    "An unidentified signal is repeating from this coordinate. Its source appears to be outside normal time.",
    "Two versions of the same event have been detected. The timeline is becoming unstable.",
    "A fragment of future data has appeared in the historical archive.",
    "A temporal echo is interfering with the laboratory's navigation system."
  ];

  anomalyText.textContent = events[Math.floor(Math.random() * events.length)];
  anomaly.classList.remove("hidden");
  addLog("TEMPORAL ANOMALY DETECTED");
}

function jump() {
  if (stability <= 0 || integrity <= 0) {
    addLog("CORE FAILURE. EXPERIMENT REQUIRES RESET.");
    return;
  }

  if (targetYear === currentYear) {
    addLog("NAVIGATION REJECTED: ALREADY AT THIS COORDINATE.");
    return;
  }

  if (anomalyActive) {
    addLog("RESOLVE THE ACTIVE ANOMALY BEFORE JUMPING.");
    return;
  }

  const distance = Math.abs(targetYear - currentYear);
  const previousYear = currentYear;

  const cost = Math.max(5, Math.ceil(distance / 35));
  stability -= Math.min(25, cost * 0.25);
  integrity -= Math.min(20, cost * 0.18);

  currentYear = targetYear;
  jumpCount++;

  yearDisplay.textContent = currentYear;
  renderTarget(currentYear);

  const era = getEra(currentYear);
  addLog(`JUMP COMPLETE: ${previousYear} → ${currentYear}`, currentYear);
  addLog(`ARRIVED IN ${era.name}`, currentYear);

  findDiscovery(currentYear);

  if (stability < 35 || integrity < 35) {
    addLog("WARNING: TEMPORAL SYSTEMS RUNNING LOW.");
  }

  maybeCreateAnomaly();
  updateMeters();
  updateMission();
  save();

  if (stability <= 0 || integrity <= 0) {
    addLog("CRITICAL FAILURE: RESET THE EXPERIMENT.");
  }
}

function resolveAnomaly() {
  if (!anomalyActive) return;

  anomalyActive = false;
  anomaly.classList.add("hidden");

  const success = Math.random() > 0.3;

  if (success) {
    stability = Math.min(100, stability + 12);
    integrity = Math.min(100, integrity + 8);
    addLog("ANOMALY CONTAINED. SYSTEMS RESTORED.");
  } else {
    stability = Math.max(0, stability - 10);
    integrity = Math.max(0, integrity - 6);
    addLog("ANOMALY PARTIALLY CONTAINED. SYSTEM DAMAGE.");
  }

  updateMeters();
  save();
}

function resetExperiment() {
  if (!confirm("Reset the experiment? All discoveries and progress will be lost.")) {
    return;
  }

  currentYear = 2026;
  targetYear = 2026;
  stability = 100;
  integrity = 100;
  found = [];
  history = [];
  jumpCount = 0;
  anomalyActive = false;

  anomaly.classList.add("hidden");
  yearDisplay.textContent = "2026";
  slider.value = 2026;

  renderTarget(2026);
  renderLog();
  updateMeters();
  save();

  addLog("NEW EXPERIMENT INITIALIZED.", 2026);
  save();
}

slider.addEventListener("input", () => {
  renderTarget(Number(slider.value));
});

document.getElementById("destinations").addEventListener("click", event => {
  const button = event.target.closest("button[data-year]");
  if (!button) return;

  const year = Number(button.dataset.year);
  slider.value = year;
  renderTarget(year);
});

jumpBtn.addEventListener("click", jump);

document.getElementById("resolveBtn").addEventListener("click", resolveAnomaly);

document.getElementById("enterBtn").addEventListener("click", () => {
  document.querySelector(".hero").classList.add("hidden");
  document.getElementById("lab").classList.remove("hidden");

  yearDisplay.textContent = currentYear;
  slider.value = currentYear;

  renderTarget(currentYear);
  renderLog();
  updateMeters();

  if (history.length === 0) {
    addLog("CHRONOS CORE INITIALIZED.", currentYear);
  }
});

document.getElementById("resetBtn").addEventListener("click", resetExperiment);

// Restore saved state.
slider.value = currentYear;
yearDisplay.textContent = currentYear;
renderTarget(currentYear);
renderLog();
updateMeters();
