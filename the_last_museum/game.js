
const $ = id => document.getElementById(id);

const artifactData = [
  {
    id: "watch",
    name: "The Forgotten Hour",
    icon: "⌚",
    category: "LOST TECHNOLOGY",
    era: "21st Century",
    description: "A mechanical wristwatch. Its hands stopped at 11:59. Someone was clearly waiting for something.",
    restored: false,
    cost: 35,
    reward: 25
  },
  {
    id: "camera",
    name: "The Memory Machine",
    icon: "📷",
    category: "LOST TECHNOLOGY",
    era: "20th Century",
    description: "A camera capable of capturing moments. Its film contains a photograph of a family whose names have disappeared.",
    restored: false,
    cost: 30,
    reward: 20
  },
  {
    id: "vase",
    name: "The Blue Vessel",
    icon: "🏺",
    category: "ANCIENT CIVILIZATION",
    era: "Ancient World",
    description: "A ceramic vessel decorated with symbols that have not yet been translated.",
    restored: false,
    cost: 40,
    reward: 30
  },
  {
    id: "seed",
    name: "The Last Seed",
    icon: "🌱",
    category: "THE NATURAL WORLD",
    era: "Pre-Collapse",
    description: "A preserved seed from a plant believed to have vanished from Earth. It may still be viable.",
    restored: false,
    cost: 45,
    reward: 35
  },
  {
    id: "key",
    name: "The Silent Key",
    icon: "🗝",
    category: "ANCIENT CIVILIZATION",
    era: "Unknown",
    description: "An unusual metal key engraved with three numbers. It may unlock something still buried.",
    restored: false,
    cost: 25,
    reward: 20
  },
  {
    id: "record",
    name: "The Last Recording",
    icon: "📼",
    category: "LOST TECHNOLOGY",
    era: "21st Century",
    description: "A damaged recording device. A few seconds of audio remain, including a voice saying: 'Remember us.'",
    restored: false,
    cost: 50,
    reward: 40
  }
];

const expeditions = [
  {
    id: "city",
    name: "The Sunken City",
    location: "Sector 07 · Coastal Ruins",
    icon: "🌊",
    cost: 30,
    description: "Search submerged buildings for lost personal belongings and technology.",
    reward: "watch"
  },
  {
    id: "temple",
    name: "The Forgotten Temple",
    location: "Sector 12 · Northern Highlands",
    icon: "🏛",
    cost: 40,
    description: "Explore an ancient structure. Its walls contain mysterious symbols.",
    reward: "vase"
  },
  {
    id: "forest",
    name: "The Silent Forest",
    location: "Sector 03 · Green Zone",
    icon: "🌲",
    cost: 35,
    description: "Search the remains of a forest for biological samples.",
    reward: "seed"
  },
  {
    id: "station",
    name: "Station Zero",
    location: "Sector 19 · Abandoned Transit",
    icon: "🚇",
    cost: 50,
    description: "A sealed underground station may contain forgotten personal objects.",
    reward: "camera"
  },
  {
    id: "vault",
    name: "The Archive Vault",
    location: "Sector 22 · Restricted Zone",
    icon: "🔐",
    cost: 65,
    description: "A mysterious underground vault. Its contents have never been catalogued.",
    reward: "record"
  }
];

const defaultState = () => ({
  credits: 100,
  reputation: 0,
  visitors: 0,
  day: 1,
  artifacts: [],
  restored: [],
  completedExpeditions: [],
  log: ["2249 — The museum has opened its doors."],
  featured: "watch"
});

function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem("last-museum-save"));
    if (saved && Array.isArray(saved.artifacts)) {
      return { ...defaultState(), ...saved };
    }
  } catch (error) {
    console.warn("Save could not be loaded:", error);
  }
  return defaultState();
}

let state = loadState();
let modalAction = null;

function save() {
  localStorage.setItem("last-museum-save", JSON.stringify(state));
  updateStats();
}

function log(message) {
  state.log.unshift(`DAY ${String(state.day).padStart(3, "0")} — ${message}`);
  state.log = state.log.slice(0, 12);
  save();
}

function hasArtifact(id) {
  return state.artifacts.includes(id);
}

function getArtifact(id) {
  return artifactData.find(item => item.id === id);
}

function updateStats() {
  $("artifactCount").textContent = state.artifacts.length;
  $("reputation").textContent = state.reputation;
  $("visitors").textContent = state.visitors;
  $("credits").textContent = state.credits;
  $("museumDate").textContent = `DAY ${String(state.day).padStart(3, "0")} · 2249`;

  $("recordArtifacts").textContent = state.artifacts.length;
  $("recordExpeditions").textContent = state.completedExpeditions.length;
  $("recordRestored").textContent = state.restored.length;
  $("recordReputation").textContent = state.reputation;

  renderCollection();
  renderExpeditions();
  renderRestoration();
  renderLog();
}

function showModal(icon, category, title, description, extra, actionText, callback) {
  $("modalIcon").textContent = icon;
  $("modalCategory").textContent = category;
  $("modalTitle").textContent = title;
  $("modalDescription").textContent = description;
  $("modalExtra").textContent = extra;
  $("modalAction").textContent = actionText;
  modalAction = callback;
  $("modal").classList.add("open");
}

function closeModal() {
  $("modal").classList.remove("open");
  modalAction = null;
}

$("closeModal").addEventListener("click", closeModal);
$("modal").addEventListener("click", event => {
  if (event.target === $("modal")) closeModal();
});
$("modalAction").addEventListener("click", () => {
  if (modalAction) modalAction();
  else closeModal();
});

function inspectArtifact(id) {
  const item = getArtifact(id);
  if (!item || !hasArtifact(id)) return;

  const isRestored = state.restored.includes(id);

  showModal(
    item.icon,
    item.category,
    item.name,
    item.description,
    `ERA: ${item.era} · ${isRestored ? "RESTORED" : "DAMAGED / UNRESTORED"}`,
    "CLOSE REPORT",
    closeModal
  );
}

function renderFeatured() {
  const item = getArtifact(state.featured);
  if (!item || !hasArtifact(item.id)) {
    const first = artifactData.find(a => hasArtifact(a.id));
    if (first) state.featured = first.id;
  }

  const featured = getArtifact(state.featured);
  if (!featured || !hasArtifact(featured.id)) {
    $("featuredArt").textContent = "◈";
    $("featuredTitle").textContent = "Awaiting Discovery";
    $("featuredDescription").textContent = "Send an expedition to recover your first artifact.";
    return;
  }

  $("featuredArt").textContent = featured.icon;
  $("featuredTitle").textContent = featured.name;
  $("featuredDescription").textContent = featured.description;
}

$("inspectFeatured").addEventListener("click", () => {
  if (hasArtifact(state.featured)) inspectArtifact(state.featured);
  else showModal("◈", "COLLECTION EMPTY", "Nothing to display", "Your featured exhibit will appear after your first successful expedition.", "", "CLOSE", closeModal);
});

function renderCollection() {
  const container = $("artifactList");
  container.innerHTML = "";

  const owned = artifactData.filter(item => hasArtifact(item.id));

  if (!owned.length) {
    container.innerHTML = '<p class="muted">Your archive is empty. Begin an expedition to recover your first artifact.</p>';
    return;
  }

  owned.forEach(item => {
    const restored = state.restored.includes(item.id);
    const row = document.createElement("div");
    row.className = "artifact-row";

    const icon = document.createElement("div");
    icon.className = "item-icon";
    icon.textContent = item.icon;

    const info = document.createElement("div");
    info.className = "item-info";

    const title = document.createElement("h3");
    title.textContent = item.name;
    const desc = document.createElement("p");
    desc.textContent = item.description;
    const tag = document.createElement("span");
    tag.className = "item-tag";
    tag.textContent = `${item.category} · ${restored ? "RESTORED" : "UNRESTORED"}`;

    info.append(title, desc, tag);

    const action = document.createElement("button");
    action.className = "item-action";
    action.textContent = "INSPECT";
    action.addEventListener("click", () => inspectArtifact(item.id));

    row.append(icon, info, action);
    container.append(row);
  });
}

function renderExpeditions() {
  const container = $("expeditionList");
  container.innerHTML = "";

  expeditions.forEach(expedition => {
    const completed = state.completedExpeditions.includes(expedition.id);
    const reward = getArtifact(expedition.reward);
    const alreadyOwned = hasArtifact(expedition.reward);

    const card = document.createElement("div");
    card.className = "expedition-card";

    const icon = document.createElement("div");
    icon.className = "item-icon";
    icon.textContent = expedition.icon;

    const info = document.createElement("div");
    info.className = "item-info";

    const title = document.createElement("h3");
    title.textContent = expedition.name;
    const desc = document.createElement("p");
    desc.textContent = expedition.description;
    const tag = document.createElement("span");
    tag.className = "item-tag";
    tag.textContent = `${expedition.location} · ${expedition.cost} CREDITS`;

    info.append(title, desc, tag);

    const action = document.createElement("button");
    action.className = "item-action";

    if (completed) {
      action.textContent = "COMPLETED";
      action.disabled = true;
    } else {
      action.textContent = "DEPLOY TEAM";
      action.addEventListener("click", () => startExpedition(expedition.id));
    }

    if (alreadyOwned && !completed) {
      tag.textContent += " · DUPLICATE REWARD POSSIBLE";
    }

    card.append(icon, info, action);
    container.append(card);
  });
}

function startExpedition(id) {
  const expedition = expeditions.find(e => e.id === id);
  if (!expedition) return;

  if (state.completedExpeditions.includes(id)) {
    return;
  }

  if (state.credits < expedition.cost) {
    showModal("⚠", "INSUFFICIENT FUNDS", "Expedition denied", "Your museum does not have enough archive credits. Restore and exhibit artifacts to earn more.", "", "CLOSE", closeModal);
    return;
  }

  showModal(
    expedition.icon,
    "EXPEDITION PROPOSAL",
    expedition.name,
    expedition.description,
    `DEPLOYMENT COST: ${expedition.cost} CREDITS`,
    "CONFIRM DEPLOYMENT",
    () => {
      closeModal();
      state.credits -= expedition.cost;
      state.day++;

      const reward = getArtifact(expedition.reward);
      const success = Math.random() < 0.85;

      state.completedExpeditions.push(id);

      if (success) {
        if (!hasArtifact(reward.id)) {
          state.artifacts.push(reward.id);
          state.featured = reward.id;
          state.reputation += 10;
          log(`Recovered ${reward.name}.`);
          showModal(reward.icon, "SUCCESSFUL RECOVERY", reward.name, reward.description, `+10 REPUTATION · ${reward.category}`, "ADD TO ARCHIVE", () => {
            closeModal();
            save();
            switchPage("collection");
          });
        } else {
          state.credits += 25;
          state.reputation += 5;
          log(`Duplicate discovery of ${reward.name}.`);
          showModal("✧", "ADDITIONAL FINDINGS", "Duplicate artifact found", "Your team recovered an additional specimen. It has been converted into archive credits.", "+25 CREDITS · +5 REPUTATION", "CONTINUE", closeModal);
        }
      } else {
        log(`Expedition to ${expedition.name} returned without a recovery.`);
        showModal("⚠", "EXPEDITION REPORT", "No artifact recovered", "The team encountered unexpected conditions. No artifact could be recovered this time.", "DEPLOYMENT COST LOST", "CONTINUE", closeModal);
      }

      save();
    }
  );
}

function renderRestoration() {
  const container = $("restorationList");
  container.innerHTML = "";

  const owned = artifactData.filter(item => hasArtifact(item.id));

  if (!owned.length) {
    container.innerHTML = '<p class="muted">No artifacts available for restoration. Recover an artifact first.</p>';
    return;
  }

  owned.forEach(item => {
    const restored = state.restored.includes(item.id);
    const row = document.createElement("div");
    row.className = "artifact-row";

    const icon = document.createElement("div");
    icon.className = "item-icon";
    icon.textContent = item.icon;

    const info = document.createElement("div");
    info.className = "item-info";

    const title = document.createElement("h3");
    title.textContent = item.name;
    const desc = document.createElement("p");
    desc.textContent = restored ? "This artifact has been successfully restored." : "The conservation team can repair this artifact and reveal more of its history.";
    const tag = document.createElement("span");
    tag.className = "item-tag";
    tag.textContent = restored ? "RESTORATION COMPLETE" : `RESTORATION COST: ${item.cost} CREDITS`;

    info.append(title, desc, tag);

    const action = document.createElement("button");
    action.className = "item-action";
    action.textContent = restored ? "RESTORED" : "RESTORE";
    action.disabled = restored;

    if (!restored) {
      action.addEventListener("click", () => restoreArtifact(item.id));
    }

    row.append(icon, info, action);
    container.append(row);
  });
}

function restoreArtifact(id) {
  const item = getArtifact(id);
  if (!item || !hasArtifact(id) || state.restored.includes(id)) return;

  if (state.credits < item.cost) {
    showModal("⚠", "INSUFFICIENT FUNDS", "Restoration unavailable", "Your conservation department needs more archive credits.", "", "CLOSE", closeModal);
    return;
  }

  showModal(
    item.icon,
    "CONSERVATION PROPOSAL",
    `Restore ${item.name}?`,
    "Your conservation team will carefully repair the artifact and preserve its recovered history.",
    `COST: ${item.cost} CREDITS · REWARD: ${item.reward} CREDITS`,
    "BEGIN RESTORATION",
    () => {
      closeModal();
      state.credits -= item.cost;
      state.restored.push(id);
      state.credits += item.reward;
      state.reputation += 15;
      state.day++;

      log(`Restored ${item.name}.`);
      save();

      showModal("✧", "RESTORATION COMPLETE", item.name, "The artifact has been carefully restored. Its story can now be shared with the public.", `+${item.reward} CREDITS · +15 REPUTATION`, "VIEW ARCHIVE", () => {
        closeModal();
        switchPage("collection");
      });
    }
  );
}

function renderLog() {
  $("eventLog").innerHTML = "";
  state.log.forEach(message => {
    const row = document.createElement("div");
    row.textContent = "› " + message;
    $("eventLog").append(row);
  });
}

function switchPage(page) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));

  const target = $(`page-${page}`);
  if (target) target.classList.add("active");

  const nav = document.querySelector(`[data-page="${page}"]`);
  if (nav) nav.classList.add("active");

  renderFeatured();
  updateStats();
}

document.querySelectorAll(".nav-btn").forEach(button => {
  button.addEventListener("click", () => switchPage(button.dataset.page));
});

document.querySelectorAll(".gallery-card").forEach(button => {
  button.addEventListener("click", () => {
    const category = button.dataset.gallery;
    const names = {
      technology: "Lost Technology",
      civilization: "Ancient Civilization",
      nature: "The Natural World"
    };

    const matching = artifactData.filter(item =>
      item.category === names[category] && hasArtifact(item.id)
    );

    if (!matching.length) {
      showModal("◈", "GALLERY EMPTY", names[category], "No artifacts have been recovered for this gallery yet. Send an expedition to discover something for this collection.", "", "EXPLORE EXPEDITIONS", () => {
        closeModal();
        switchPage("expedition");
      });
      return;
    }

    const item = matching[0];
    inspectArtifact(item.id);
  });
});

$("enterMuseum").addEventListener("click", () => {
  document.querySelector(".museum").scrollIntoView({ behavior: "smooth" });
});

$("saveButton").addEventListener("click", () => {
  save();
  showModal("✓", "ARCHIVE SYSTEM", "Museum saved", "Your collection, credits, expeditions and restoration records have been saved in this browser.", "", "CONTINUE", closeModal);
});

$("resetButton").addEventListener("click", () => {
  if (!confirm("Permanently reset your museum and all its progress?")) return;
  state = defaultState();
  save();
  switchPage("gallery");
  showModal("◈", "NEW BEGINNING", "The museum has been reset", "A new archive awaits its curator.", "", "ENTER", closeModal);
});

function dailyVisitors() {
  if (state.artifacts.length > 0) {
    const gain = Math.floor(state.artifacts.length * 3 + state.reputation / 10);
    state.visitors += gain;
    state.credits += Math.floor(gain / 4);
  }
}

// Simulated museum visitor cycle.
setInterval(() => {
  dailyVisitors();
  updateStats();
  save();
}, 30000);

renderFeatured();
updateStats();
