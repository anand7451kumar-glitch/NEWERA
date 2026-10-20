
const $ = (id) => document.getElementById(id);

const modes = {
  focus: { label: "Focus", seconds: 25 * 60, caption: "Time to concentrate" },
  short: { label: "Short break", seconds: 5 * 60, caption: "Take a breather" },
  long: { label: "Long break", seconds: 15 * 60, caption: "Recharge your mind" }
};

let mode = "focus";
let remaining = modes.focus.seconds;
let timerId = null;
let endTime = null;
let running = false;

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    }
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong");
  }

  return data;
}

function showError(error) {
  $("timerMessage").textContent = error.message;
}

function renderTimer() {
  const minutes = Math.floor(remaining / 60);
  const seconds = remaining % 60;

  $("timer").textContent =
    `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

  $("timerCaption").textContent = modes[mode].caption;
  $("timerModeLabel").textContent = modes[mode].label;
  $("startBtn").textContent = running ? "Ⅱ Pause" :
    remaining === modes[mode].seconds ? "▶ Start focus" : "▶ Resume";

  const fraction = 1 - remaining / modes[mode].seconds;
  const degrees = Math.max(0, Math.min(360, fraction * 360));

  $("timerRing").style.background =
    `radial-gradient(circle, var(--panel) 65%, transparent 66%),
     conic-gradient(var(--accent) ${degrees}deg, #37344b ${degrees}deg)`;

  document.title = `${$("timer").textContent} · FocusFlow`;
}

function stopTimer() {
  clearInterval(timerId);
  timerId = null;
  running = false;
  endTime = null;
}

function chooseMode(nextMode) {
  if (running) return;

  mode = nextMode;
  remaining = modes[mode].seconds;

  document.querySelectorAll(".mode").forEach(button => {
    button.classList.toggle("selected", button.dataset.mode === mode);
  });

  $("timerMessage").textContent = "Ready when you are.";
  renderTimer();
}

async function completeSession() {
  stopTimer();
  remaining = 0;
  renderTimer();

  $("timerMessage").textContent = "Saving your completed session...";

  try {
    await api("/api/sessions", {
      method: "POST",
      body: JSON.stringify({
        mode,
        minutes: modes[mode].seconds / 60
      })
    });

    $("timerMessage").textContent =
      mode === "focus" ? "Focus session complete. Take a break!" : "Break complete. Well done!";
    await loadStats();
  } catch (error) {
    $("timerMessage").textContent =
      "Session finished, but saving failed: " + error.message;
  }
}

function tick() {
  remaining = Math.max(0, Math.ceil((endTime - Date.now()) / 1000));

  if (remaining <= 0) {
    completeSession();
    return;
  }

  renderTimer();
}

$("startBtn").addEventListener("click", () => {
  if (running) {
    remaining = Math.max(0, Math.ceil((endTime - Date.now()) / 1000));
    stopTimer();
    $("timerMessage").textContent = "Timer paused.";
    renderTimer();
    return;
  }

  if (remaining <= 0) remaining = modes[mode].seconds;

  running = true;
  endTime = Date.now() + remaining * 1000;
  $("timerMessage").textContent = "Stay focused. You've got this.";
  timerId = setInterval(tick, 250);
  renderTimer();
});

$("resetBtn").addEventListener("click", () => {
  stopTimer();
  remaining = modes[mode].seconds;
  $("timerMessage").textContent = "Timer reset.";
  renderTimer();
});

document.querySelectorAll(".mode").forEach(button => {
  button.addEventListener("click", () => chooseMode(button.dataset.mode));
});

async function loadTasks() {
  const tasks = await api("/api/tasks");
  const list = $("taskList");

  list.replaceChildren();

  if (tasks.length === 0) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No tasks yet. Add your first goal above.";
    list.append(empty);
  }

  for (const task of tasks) {
    const item = document.createElement("div");
    item.className = "task-item" + (task.completed ? " done" : "");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = Boolean(task.completed);
    checkbox.setAttribute("aria-label", "Mark task complete");

    checkbox.addEventListener("change", async () => {
      checkbox.disabled = true;
      try {
        await api(`/api/tasks/${task.id}`, {
          method: "PATCH",
          body: JSON.stringify({ completed: checkbox.checked })
        });
        await loadTasks();
        await loadStats();
      } catch (error) {
        checkbox.checked = !checkbox.checked;
        checkbox.disabled = false;
        showError(error);
      }
    });

    const main = document.createElement("div");
    main.className = "task-main";

    const title = document.createElement("div");
    title.className = "task-title";
    title.textContent = task.title;

    const meta = document.createElement("div");
    meta.className = "task-meta";
    meta.textContent = task.due_date ? `Due ${task.due_date}` : "No due date";

    main.append(title, meta);

    const badge = document.createElement("span");
    badge.className = `priority ${task.priority}`;
    badge.textContent = task.priority;

    const remove = document.createElement("button");
    remove.className = "delete-btn";
    remove.textContent = "×";
    remove.setAttribute("aria-label", "Delete task");

    remove.addEventListener("click", async () => {
      if (!confirm(`Delete "${task.title}"?`)) return;

      try {
        await api(`/api/tasks/${task.id}`, { method: "DELETE" });
        await loadTasks();
        await loadStats();
      } catch (error) {
        showError(error);
      }
    });

    item.append(checkbox, main, badge, remove);
    list.append(item);
  }

  const completed = tasks.filter(task => task.completed).length;
  $("taskBadge").textContent = `${completed}/${tasks.length} done`;
}

$("taskForm").addEventListener("submit", async event => {
  event.preventDefault();

  const title = $("taskInput").value.trim();
  if (!title) return;

  try {
    await api("/api/tasks", {
      method: "POST",
      body: JSON.stringify({
        title,
        priority: $("priority").value,
        dueDate: $("dueDate").value
      })
    });

    $("taskInput").value = "";
    $("priority").value = "Normal";
    $("dueDate").value = "";

    await loadTasks();
    await loadStats();
  } catch (error) {
    showError(error);
  }
});

function renderChart(week) {
  const chart = $("weeklyChart");
  chart.replaceChildren();

  const values = new Map(week.map(item => [item.day, Number(item.minutes)]));
  const today = new Date();
  const days = [];

  for (let offset = 6; offset >= 0; offset--) {
    const day = new Date(today);
    day.setDate(today.getDate() - offset);

    const key = `${day.getFullYear()}-${String(day.getMonth() + 1).padStart(2, "0")}-${String(day.getDate()).padStart(2, "0")}`;

    days.push({
      key,
      label: day.toLocaleDateString(undefined, { weekday: "short" }),
      minutes: values.get(key) || 0
    });
  }

  const maxMinutes = Math.max(60, ...days.map(day => day.minutes));

  for (const day of days) {
    const column = document.createElement("div");
    column.className = "chart-day";

    const value = document.createElement("div");
    value.className = "bar-value";
    value.textContent = `${day.minutes}m`;

    const area = document.createElement("div");
    area.className = "bar-area";

    const bar = document.createElement("div");
    bar.className = "bar";
    bar.style.height = `${Math.max(3, day.minutes / maxMinutes * 100)}%`;
    bar.title = `${day.label}: ${day.minutes} focus minutes`;

    area.append(bar);

    const label = document.createElement("div");
    label.className = "day-label";
    label.textContent = day.label;

    column.append(value, area, label);
    chart.append(column);
  }
}

async function loadStats() {
  const stats = await api("/api/stats");

  $("focusMinutes").textContent = stats.focusMinutes;
  $("sessionCount").textContent = stats.sessionCount;
  $("taskCount").textContent = stats.taskCount;

  renderChart(stats.week);
}

async function init() {
  renderTimer();

  try {
    await Promise.all([loadTasks(), loadStats()]);
  } catch (error) {
    $("timerMessage").textContent =
      "Couldn't connect to the server. Check that server.py is running.";
    $("taskList").textContent = "Unable to load tasks. Refresh after starting the server.";
  }
}

init();
