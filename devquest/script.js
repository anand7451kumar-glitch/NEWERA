
"use strict";

// ============================================
// DEVQUEST — CODING MISSION CONTROL
// ============================================

const $ = (id) => document.getElementById(id);
const STORAGE_KEY = "devquest-save-v1";

const XP_VALUES = {
  easy: 25,
  medium: 50,
  hard: 100
};

const RANKS = [
  "Code Initiate",
  "Bug Hunter",
  "Logic Architect",
  "Code Warrior",
  "Full Stack Hero",
  "Algorithm Master",
  "Dev Legend",
  "Grand Architect"
];

const ACHIEVEMENTS = [
  {
    id: "first",
    icon: "⚡",
    title: "First Blood",
    description: "Complete your first quest",
    check: (s) => s.completed.length >= 1
  },
  {
    id: "five",
    icon: "⚔",
    title: "Quest Hunter",
    description: "Complete 5 quests",
    check: (s) => s.completed.length >= 5
  },
  {
    id: "ten",
    icon: "🏆",
    title: "Double Digits",
    description: "Complete 10 quests",
    check: (s) => s.completed.length >= 10
  },
  {
    id: "xp",
    icon: "✧",
    title: "XP Collector",
    description: "Earn 500 XP",
    check: (s) => s.xp >= 500
  },
  {
    id: "level3",
    icon: "⬡",
    title: "Rising Star",
    description: "Reach level 3",
    check: (s) => getLevel(s.xp).level >= 3
  },
  {
    id: "streak3",
    icon: "♨",
    title: "On Fire",
    description: "Code on 3 consecutive days",
    check: (s) => calculateStreak(s.activity) >= 3
  },
  {
    id: "dsa",
    icon: "⌘",
    title: "Problem Solver",
    description: "Complete a DSA quest",
    check: (s) => s.completed.some((q) => q.category === "DSA")
  },
  {
    id: "hard",
    icon: "◆",
    title: "Boss Slayer",
    description: "Complete a hard quest",
    check: (s) => s.completed.some((q) => q.difficulty === "hard")
  }
];

function localDateKey(date = new Date()) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}

function daysAgo(amount) {
  const date = new Date();
  date.setHours(12, 0, 0, 0);
  date.setDate(date.getDate() - amount);
  return date;
}

function makeId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

function createInitialState() {
  return {
    xp: 0,
    quests: [],
    completed: [],
    activity: {},
    unlocked: [],
    nextId: 1
  };
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);

    if (!raw) return createInitialState();

    const saved = JSON.parse(raw);

    if (
      !saved ||
      typeof saved !== "object" ||
      !Array.isArray(saved.quests) ||
      !Array.isArray(saved.completed) ||
      typeof saved.activity !== "object" ||
      saved.activity === null
    ) {
      return createInitialState();
    }

    return {
      xp: Math.max(0, Number(saved.xp) || 0),
      quests: saved.quests,
      completed: saved.completed,
      activity: saved.activity,
      unlocked: Array.isArray(saved.unlocked) ? saved.unlocked : [],
      nextId: Math.max(1, Number(saved.nextId) || 1)
    };
  } catch (error) {
    console.warn("Could not load DevQuest save:", error);
    return createInitialState();
  }
}

let state = loadState();
let currentFilter = "all";
let toastTimeout;
let timerInterval = null;
let timerRemaining = 25 * 60;
let selectedMinutes = 25;
let timerRunning = false;

function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    console.warn("Could not save DevQuest progress:", error);
    showToast("Your browser couldn't save progress. Check storage settings.");
  }
}

// ============================================
// LEVEL AND STREAK CALCULATIONS
// ============================================

function getLevel(xp) {
  const level = Math.floor(Math.max(0, xp) / 100) + 1;
  const progress = Math.max(0, xp) % 100;
  const rankIndex = Math.min(level - 1, RANKS.length - 1);

  return {
    level,
    progress,
    remaining: 100 - progress,
    rank: RANKS[rankIndex]
  };
}

function calculateStreak(activity) {
  const today = localDateKey();
  const yesterday = localDateKey(daysAgo(1));

  // A streak remains alive if the most recent active day was today
  // or yesterday. It does not reset just because today is unfinished.
  let cursor;

  if ((activity[today] || 0) > 0) {
    cursor = new Date();
  } else if ((activity[yesterday] || 0) > 0) {
    cursor = daysAgo(1);
  } else {
    return 0;
  }

  cursor.setHours(12, 0, 0, 0);
  let streak = 0;

  while ((activity[localDateKey(cursor)] || 0) > 0) {
    streak++;
    cursor.setDate(cursor.getDate() - 1);
  }

  return streak;
}

function getActiveDays(activity) {
  return Object.values(activity).filter((count) => count > 0).length;
}

// ============================================
// TOAST NOTIFICATIONS
// ============================================

function showToast(message) {
  const toast = $("toast");
  toast.textContent = message;
  toast.classList.add("visible");

  clearTimeout(toastTimeout);

  toastTimeout = setTimeout(() => {
    toast.classList.remove("visible");
  }, 2800);
}

// ============================================
// QUEST MANAGEMENT
// ============================================

function addQuest(event) {
  event.preventDefault();

  const input = $("questInput");
  const title = input.value.trim();
  const category = $("questCategory").value;
  const difficulty = $("questDifficulty").value;

  if (!title) {
    input.focus();
    return;
  }

  const quest = {
    id: makeId(),
    title,
    category,
    difficulty,
    xp: XP_VALUES[difficulty],
    createdAt: localDateKey(),
    completed: false
  };

  state.quests.unshift(quest);
  saveState();
  renderAll();

  input.value = "";
  input.focus();

  showToast("Quest added to your mission board.");
}

function completeQuest(id) {
  const index = state.quests.findIndex((quest) => quest.id === id);

  if (index === -1) return;

  const [quest] = state.quests.splice(index, 1);

  const completedQuest = {
    ...quest,
    completed: true,
    completedAt: localDateKey()
  };

  state.completed.unshift(completedQuest);
  state.xp += quest.xp;

  const today = localDateKey();
  state.activity[today] = (state.activity[today] || 0) + 1;

  checkAchievements();
  saveState();
  renderAll();

  showToast(`Quest cleared! +${quest.xp} XP earned.`);
}

function deleteQuest(id) {
  const activeIndex = state.quests.findIndex((quest) => quest.id === id);

  if (activeIndex !== -1) {
    state.quests.splice(activeIndex, 1);
    saveState();
    renderAll();
    showToast("Quest removed.");
    return;
  }

  const completedIndex = state.completed.findIndex((quest) => quest.id === id);

  if (completedIndex !== -1) {
    const [quest] = state.completed.splice(completedIndex, 1);
    state.xp = Math.max(0, state.xp - quest.xp);

    const date = quest.completedAt;

    if (date && state.activity[date]) {
      state.activity[date]--;

      if (state.activity[date] <= 0) {
        delete state.activity[date];
      }
    }

    checkAchievements();
    saveState();
    renderAll();

    showToast("Completed quest removed; its XP was reversed.");
  }
}

function getVisibleQuests() {
  if (currentFilter === "active") return state.quests;
  if (currentFilter === "completed") return state.completed;

  return [...state.quests, ...state.completed];
}

function renderQuests() {
  const list = $("questList");
  const empty = $("emptyState");
  const quests = getVisibleQuests();

  list.replaceChildren();

  $("questCount").textContent = `${state.quests.length} ACTIVE`;
  $("questSummary").textContent =
    `${state.completed.length} cleared · ${state.quests.length} active`;

  empty.classList.toggle("hidden", quests.length > 0);

  if (quests.length === 0) {
    $("emptyState").querySelector("h3").textContent =
      currentFilter === "completed" ? "No quests cleared yet" :
      currentFilter === "active" ? "All caught up!" :
      "No quests on your radar";

    $("emptyState").querySelector("p").textContent =
      currentFilter === "completed"
        ? "Complete a mission to see it here."
        : currentFilter === "active"
          ? "Add a new quest when you're ready."
          : "Add your first mission above and start earning XP.";

    return;
  }

  quests.forEach((quest) => {
    const isCompleted = quest.completed === true ||
      state.completed.some((item) => item.id === quest.id);

    const row = document.createElement("div");
    row.className = `quest-item${isCompleted ? " completed" : ""}`;

    const check = document.createElement("button");
    check.className = "quest-check";
    check.type = "button";
    check.textContent = "✓";
    check.setAttribute(
      "aria-label",
      isCompleted ? `Completed: ${quest.title}` : `Complete: ${quest.title}`
    );

    if (isCompleted) {
      check.disabled = true;
      check.title = "Already completed";
    } else {
      check.addEventListener("click", () => completeQuest(quest.id));
    }

    const details = document.createElement("div");
    details.className = "quest-details";

    const title = document.createElement("p");
    title.className = "quest-title";
    title.textContent = quest.title;

    const meta = document.createElement("div");
    meta.className = "quest-meta";

    const category = document.createElement("span");
    category.className = "category-tag";
    category.textContent = quest.category;

    const difficulty = document.createElement("span");
    difficulty.className = `difficulty-tag ${quest.difficulty}`;
    difficulty.textContent =
      quest.difficulty.charAt(0).toUpperCase() + quest.difficulty.slice(1);

    meta.append(category, difficulty);
    details.append(title, meta);

    const right = document.createElement("div");
    right.className = "quest-right";

    const xp = document.createElement("span");
    xp.className = "quest-xp";
    xp.textContent = `+${quest.xp} XP`;

    const remove = document.createElement("button");
    remove.className = "delete-quest";
    remove.type = "button";
    remove.textContent = "×";
    remove.title = "Delete quest";
    remove.setAttribute("aria-label", `Delete ${quest.title}`);
    remove.addEventListener("click", () => deleteQuest(quest.id));

    right.append(xp, remove);
    row.append(check, details, right);
    list.append(row);
  });
}

// ============================================
// STATS AND LEVEL PROGRESS
// ============================================

function renderStats() {
  const level = getLevel(state.xp);
  const totalQuests = state.quests.length + state.completed.length;
  const completionRate = totalQuests > 0
    ? Math.round((state.completed.length / totalQuests) * 100)
    : 0;

  $("totalXP").innerHTML = `${state.xp.toLocaleString()} <span>XP</span>`;
  $("currentLevel").textContent = String(level.level).padStart(2, "0");
  $("levelTitle").textContent = level.rank;
  $("completedQuests").textContent = state.completed.length;
  $("completionRate").textContent = `${completionRate}%`;
  $("currentStreak").innerHTML =
    `${calculateStreak(state.activity)} <span>days</span>`;

  $("xpMiniBar").style.width = `${Math.min(100, state.xp % 100)}%`;
  $("levelMiniBar").style.width = `${level.progress}%`;
  $("questMiniBar").style.width = `${completionRate}%`;

  $("levelBadge").textContent = `LV. ${String(level.level).padStart(2, "0")}`;
  $("rankName").textContent = level.rank;
  $("levelProgressText").textContent = `${level.progress} / 100 XP`;
  $("nextLevelText").textContent = `${level.remaining} XP to next level`;
  $("levelProgressBar").style.width = `${level.progress}%`;

  const dots = $("streakDots");
  dots.replaceChildren();

  for (let i = 6; i >= 0; i--) {
    const dateKey = localDateKey(daysAgo(i));
    const dot = document.createElement("span");

    if ((state.activity[dateKey] || 0) > 0) {
      dot.classList.add("active");
    }

    dot.title = `${dateKey}: ${state.activity[dateKey] || 0} quests completed`;
    dots.append(dot);
  }
}

// ============================================
// ACTIVITY HEATMAP
// ============================================

function renderHeatmap() {
  const heatmap = $("heatmap");
  heatmap.replaceChildren();

  const today = new Date();
  today.setHours(12, 0, 0, 0);

  // Show 12 weeks, ending today.
  const start = new Date(today);
  start.setDate(start.getDate() - 83);

  // Align the start to Sunday so each column is one calendar week.
  start.setDate(start.getDate() - start.getDay());

  const activeDates = new Set();

  for (let i = 0; i < 84; i++) {
    const date = new Date(start);
    date.setDate(start.getDate() + i);

    if (date > today) continue;

    const key = localDateKey(date);
    const count = state.activity[key] || 0;
    const level = count === 0 ? 0 : count === 1 ? 1 : count === 2 ? 2 : count <= 4 ? 3 : 4;

    const cell = document.createElement("div");
    cell.className = "heat-cell";
    cell.dataset.level = String(level);
    cell.title = `${key}: ${count} quest${count === 1 ? "" : "s"} completed`;
    cell.setAttribute("role", "img");
    cell.setAttribute("aria-label", cell.title);

    heatmap.append(cell);

    if (count > 0) activeDates.add(key);
  }

  $("activeDays").textContent = getActiveDays(state.activity);
  $("activitySummary").textContent = activeDates.size > 0
    ? `${activeDates.size} active day${activeDates.size === 1 ? "" : "s"} recorded in your journey.`
    : "Every quest counts. Start your first today.";
}

// ============================================
// ACHIEVEMENTS
// ============================================

function checkAchievements() {
  const newlyUnlocked = [];

  for (const achievement of ACHIEVEMENTS) {
    if (
      achievement.check(state) &&
      !state.unlocked.includes(achievement.id)
    ) {
      state.unlocked.push(achievement.id);
      newlyUnlocked.push(achievement);
    }
  }

  newlyUnlocked.forEach((achievement) => {
    showToast(`Achievement unlocked: ${achievement.title}!`);
  });
}

function renderAchievements() {
  const grid = $("achievementGrid");
  grid.replaceChildren();

  const unlockedCount = ACHIEVEMENTS.filter((achievement) =>
    state.unlocked.includes(achievement.id)
  ).length;

  $("achievementCount").textContent = `${unlockedCount} UNLOCKED`;

  ACHIEVEMENTS.forEach((achievement) => {
    const unlocked = state.unlocked.includes(achievement.id);

    const card = document.createElement("article");
    card.className = `achievement-card${unlocked ? " unlocked" : ""}`;

    const icon = document.createElement("div");
    icon.className = "achievement-icon";
    icon.textContent = achievement.icon;

    const title = document.createElement("h3");
    title.textContent = achievement.title;

    const description = document.createElement("p");
    description.textContent = achievement.description;

    const status = document.createElement("span");
    status.className = "achievement-status";
    status.textContent = unlocked ? "✓ UNLOCKED" : "◈ LOCKED";

    card.append(icon, title, description, status);
    grid.append(card);
  });
}

// ============================================
// FOCUS TIMER
// ============================================

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainder = seconds % 60;

  return `${String(minutes).padStart(2, "0")}:${String(remainder).padStart(2, "0")}`;
}

function renderTimer() {
  $("focusTimer").textContent = formatTime(timerRemaining);
  $("timerStart").textContent = timerRunning ? "Pause focus" : "Start focus";
  $("timerStatus").textContent = timerRunning
    ? "Stay focused. You've got this."
    : timerRemaining === 0
      ? "Session complete. Take a breath."
      : "Ready when you are.";

  document.title = timerRunning
    ? `${formatTime(timerRemaining)} · DevQuest`
    : "DevQuest — Coding Mission Control";
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }

  timerRunning = false;
}

function tickTimer() {
  if (timerRemaining > 0) {
    timerRemaining--;
    renderTimer();
  }

  if (timerRemaining === 0) {
    stopTimer();
    renderTimer();
    showToast("Focus session complete. Nice work!");
  }
}

function toggleTimer() {
  if (timerRunning) {
    stopTimer();
    renderTimer();
    return;
  }

  if (timerRemaining <= 0) {
    timerRemaining = selectedMinutes * 60;
  }

  timerRunning = true;
  renderTimer();

  timerInterval = setInterval(tickTimer, 1000);
}

function selectTimerPreset(minutes, button) {
  stopTimer();
  selectedMinutes = minutes;
  timerRemaining = minutes * 60;

  document.querySelectorAll(".timer-preset").forEach((preset) => {
    preset.classList.toggle("active", preset === button);
  });

  renderTimer();
}

function resetTimer() {
  stopTimer();
  timerRemaining = selectedMinutes * 60;
  renderTimer();
}

// ============================================
// DATE AND NAVIGATION
// ============================================

function renderDate() {
  $("currentDate").textContent = new Intl.DateTimeFormat("en-IN", {
    weekday: "short",
    day: "numeric",
    month: "short",
    year: "numeric"
  }).format(new Date()).toUpperCase();
}

function setupNavigation() {
  document.querySelectorAll(".nav-link").forEach((link) => {
    link.addEventListener("click", () => {
      document.querySelectorAll(".nav-link").forEach((item) => {
        item.classList.toggle("active", item === link);
      });
    });
  });
}

// ============================================
// RENDER EVERYTHING
// ============================================

function renderAll() {
  renderQuests();
  renderStats();
  renderHeatmap();
  renderAchievements();
  renderTimer();
}

function setupEventListeners() {
  $("questForm").addEventListener("submit", addQuest);

  document.querySelectorAll(".filter-tab").forEach((button) => {
    button.addEventListener("click", () => {
      currentFilter = button.dataset.filter;

      document.querySelectorAll(".filter-tab").forEach((tab) => {
        tab.classList.toggle("active", tab === button);
      });

      renderQuests();
    });
  });

  $("timerStart").addEventListener("click", toggleTimer);
  $("timerReset").addEventListener("click", resetTimer);

  document.querySelectorAll(".timer-preset").forEach((button) => {
    button.addEventListener("click", () => {
      selectTimerPreset(Number(button.dataset.minutes), button);
    });
  });
}

// ============================================
// STARTUP
// ============================================

function init() {
  checkAchievements();
  setupEventListeners();
  setupNavigation();
  renderDate();
  renderAll();
  saveState();
}

init();
