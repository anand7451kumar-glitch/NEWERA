
// ==========================================
// ATTENDIQ — SMART ATTENDANCE PLANNER
// ==========================================

// 1. ELEMENT HELPERS

const $ = (id) => document.getElementById(id);

const STORAGE_KEY = "attendiq-data-v1";

let subjects = [];
let history = [];
let target = 75;
let editingSubjectId = null;


// 2. LOAD AND SAVE DATA

function loadData() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");

    subjects = Array.isArray(saved.subjects)
      ? saved.subjects.filter((subject) =>
          subject &&
          typeof subject.id === "string" &&
          typeof subject.name === "string" &&
          Number.isInteger(subject.attended) &&
          Number.isInteger(subject.missed) &&
          subject.attended >= 0 &&
          subject.missed >= 0
        )
      : [];

    history = Array.isArray(saved.history)
      ? saved.history.filter((item) =>
          item &&
          typeof item.subjectName === "string" &&
          (item.status === "Attended" || item.status === "Missed") &&
          typeof item.date === "string"
        ).slice(0, 100)
      : [];

    target = Number.isFinite(saved.target)
      ? Math.min(100, Math.max(1, saved.target))
      : 75;

  } catch (error) {
    console.error("Could not load AttendIQ data:", error);
    subjects = [];
    history = [];
    target = 75;
  }
}

function saveData() {
  try {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        subjects,
        history,
        target
      })
    );
  } catch (error) {
    console.error("Could not save AttendIQ data:", error);
    showToast("Unable to save data. Check browser storage.");
  }
}


// 3. BASIC CALCULATIONS

function getTotalClasses(subject) {
  return subject.attended + subject.missed;
}

function getPercentage(subject) {
  const total = getTotalClasses(subject);

  if (total === 0) return 0;

  return (subject.attended / total) * 100;
}

function getOverallStats() {
  const attended = subjects.reduce(
    (sum, subject) => sum + subject.attended,
    0
  );

  const missed = subjects.reduce(
    (sum, subject) => sum + subject.missed,
    0
  );

  const total = attended + missed;

  return {
    attended,
    missed,
    total,
    percentage: total > 0 ? (attended / total) * 100 : 0
  };
}

function formatPercentage(value) {
  return `${value.toFixed(1)}%`;
}

function getSubjectStatus(subject) {
  const percentage = getPercentage(subject);

  if (getTotalClasses(subject) === 0) {
    return "No classes recorded";
  }

  return percentage >= target
    ? "On track"
    : "Below target";
}


// 4. DATE AND TOAST

function renderDate() {
  $("currentDate").textContent =
    new Date().toLocaleDateString("en-IN", {
      weekday: "short",
      day: "numeric",
      month: "short",
      year: "numeric"
    });
}

let toastTimeout;

function showToast(message) {
  const toast = $("toast");

  toast.textContent = message;
  toast.classList.add("show");

  clearTimeout(toastTimeout);

  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 2500);
}


// 5. OVERVIEW DASHBOARD

function renderOverview() {
  const stats = getOverallStats();

  $("overallPercentage").textContent =
    stats.total > 0 ? stats.percentage.toFixed(1) : "0";

  $("ringPercentage").textContent =
    stats.total > 0 ? formatPercentage(stats.percentage) : "0%";

  $("totalAttended").textContent = stats.attended;
  $("totalMissed").textContent = stats.missed;
  $("totalClasses").textContent = stats.total;
  $("totalSubjects").textContent = subjects.length;

  $("targetLabel").textContent = `Target: ${target}%`;

  $("defaultTarget").value = target;

  $("overallProgress").style.width =
    `${Math.min(100, stats.percentage)}%`;

  const degrees = (stats.percentage / 100) * 360;

  $("attendanceRing").style.background =
    `conic-gradient(var(--green) 0deg ${degrees}deg, #304238 ${degrees}deg 360deg)`;

  if (stats.total === 0) {
    $("overallMessage").textContent =
      "Add your subjects and start recording classes.";
  } else if (stats.percentage >= target) {
    $("overallMessage").textContent =
      `Great work! You're meeting your ${target}% attendance target.`;
  } else {
    $("overallMessage").textContent =
      `You're ${(target - stats.percentage).toFixed(1)} percentage points below your target.`;
  }
}


// 6. SUBJECT FORM

function openSubjectForm(subject = null) {
  editingSubjectId = subject ? subject.id : null;

  $("subjectFormCard").classList.remove("hidden");

  $("subjectName").value = subject ? subject.name : "";
  $("subjectCode").value = subject ? subject.code : "";

  $("initialAttended").value = subject ? subject.attended : 0;
  $("initialMissed").value = subject ? subject.missed : 0;

  const heading = $("subjectFormCard").querySelector("h3");

  heading.textContent = subject ? "Edit subject" : "Add a subject";

  $("subjectFormCard").scrollIntoView({
    behavior: "smooth",
    block: "center"
  });

  $("subjectName").focus();
}

function closeSubjectForm() {
  $("subjectFormCard").classList.add("hidden");
  $("subjectForm").reset();

  editingSubjectId = null;
}

function handleSubjectSubmit(event) {
  event.preventDefault();

  const name = $("subjectName").value.trim();
  const code = $("subjectCode").value.trim();

  const attended = Number($("initialAttended").value);
  const missed = Number($("initialMissed").value);

  if (!name) {
    showToast("Enter a subject name.");
    return;
  }

  if (
    !Number.isSafeInteger(attended) ||
    !Number.isSafeInteger(missed) ||
    attended < 0 ||
    missed < 0 ||
    attended > 10000 ||
    missed > 10000
  ) {
    showToast("Enter valid class counts.");
    return;
  }

  if (editingSubjectId) {
    const subject = subjects.find(
      (item) => item.id === editingSubjectId
    );

    if (!subject) return;

    subject.name = name;
    subject.code = code;
    subject.attended = attended;
    subject.missed = missed;

    showToast("Subject updated.");
  } else {
    subjects.push({
      id: crypto.randomUUID(),
      name,
      code,
      attended,
      missed
    });

    if (attended > 0 || missed > 0) {
      history.unshift({
        subjectName: name,
        date: new Date().toISOString(),
        status: "Initial record",
        count: attended + missed
      });
    }

    showToast("Subject added successfully.");
  }

  closeSubjectForm();
  saveData();
  renderAll();
}


// 7. SUBJECT CARDS

function renderSubjects() {
  const grid = $("subjectsGrid");
  const filter = $("subjectFilter").value;

  grid.replaceChildren();

  const filteredSubjects = subjects.filter((subject) => {
    const percentage = getPercentage(subject);

    if (filter === "safe") {
      return getTotalClasses(subject) > 0 && percentage >= target;
    }

    if (filter === "warning") {
      return getTotalClasses(subject) > 0 && percentage < target;
    }

    return true;
  });

  $("subjectCount").textContent =
    `${filteredSubjects.length} of ${subjects.length} subjects`;

  if (filteredSubjects.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-state";

    const icon = document.createElement("div");
    icon.className = "empty-icon";
    icon.textContent = "▤";

    const heading = document.createElement("h3");
    heading.textContent = subjects.length === 0
      ? "No subjects yet"
      : "No matching subjects";

    const message = document.createElement("p");
    message.textContent = subjects.length === 0
      ? "Add your first subject to start monitoring attendance."
      : "Try changing your subject filter.";

    empty.append(icon, heading, message);

    if (subjects.length === 0) {
      const button = document.createElement("button");
      button.className = "primary-button";
      button.textContent = "＋ Add your first subject";
      button.addEventListener("click", () => openSubjectForm());
      empty.appendChild(button);
    }

    grid.appendChild(empty);
    return;
  }

  filteredSubjects.forEach((subject) => {
    const percentage = getPercentage(subject);
    const total = getTotalClasses(subject);
    const safe = total > 0 && percentage >= target;

    const card = document.createElement("article");
    card.className = "subject-card";

    // Subject heading
    const top = document.createElement("div");
    top.className = "subject-card-top";

    const identity = document.createElement("div");

    const name = document.createElement("h3");
    name.className = "subject-name";
    name.textContent = subject.name;

    const code = document.createElement("span");
    code.className = "subject-code";
    code.textContent = subject.code || "No subject code";

    identity.append(name, code);

    const percent = document.createElement("strong");
    percent.className = `subject-percentage ${safe ? "" : "warning"}`;
    percent.textContent = formatPercentage(percentage);

    top.append(identity, percent);

    // Progress bar
    const progress = document.createElement("div");
    progress.className = "subject-progress";

    const fill = document.createElement("div");
    fill.className = `subject-progress-fill ${safe ? "" : "warning"}`;
    fill.style.width = `${Math.min(100, percentage)}%`;

    progress.appendChild(fill);

    // Class numbers
    const meta = document.createElement("div");
    meta.className = "subject-meta";

    const attended = document.createElement("span");
    attended.textContent = `Attended: ${subject.attended}`;

    const missed = document.createElement("span");
    missed.textContent = `Missed: ${subject.missed}`;

    meta.append(attended, missed);

    // Status
    const status = document.createElement("span");
    status.className = `subject-status ${safe ? "" : "warning"}`;
    status.textContent = total === 0
      ? "No classes recorded"
      : safe
        ? "✓ On track"
        : "⚠ Below target";

    // Actions
    const actions = document.createElement("div");
    actions.className = "subject-actions";

    const attendButton = document.createElement("button");
    attendButton.textContent = "+ Attended";
    attendButton.addEventListener("click", () => {
      recordClass(subject.id, "Attended");
    });

    const missButton = document.createElement("button");
    missButton.className = "miss-button";
    missButton.textContent = "+ Missed";
    missButton.addEventListener("click", () => {
      recordClass(subject.id, "Missed");
    });

    const editButton = document.createElement("button");
    editButton.textContent = "Edit";
    editButton.addEventListener("click", () => {
      openSubjectForm(subject);
    });

    const deleteButton = document.createElement("button");
    deleteButton.className = "delete-button";
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => {
      deleteSubject(subject.id);
    });

    actions.append(
      attendButton,
      missButton,
      editButton,
      deleteButton
    );

    card.append(top, progress, meta, status, actions);
    grid.appendChild(card);
  });
}


// 8. RECORD ATTENDANCE

function recordClass(id, status) {
  const subject = subjects.find((item) => item.id === id);

  if (!subject) return;

  if (status === "Attended") {
    subject.attended++;
  } else {
    subject.missed++;
  }

  history.unshift({
    subjectName: subject.name,
    date: new Date().toISOString(),
    status,
    count: 1
  });

  history = history.slice(0, 100);

  saveData();
  renderAll();

  showToast(
    `${subject.name}: ${status.toLowerCase()} class recorded.`
  );
}


// 9. DELETE SUBJECT

function deleteSubject(id) {
  const subject = subjects.find((item) => item.id === id);

  if (!subject) return;

  const confirmed = window.confirm(
    `Delete "${subject.name}" and its attendance records?`
  );

  if (!confirmed) return;

  subjects = subjects.filter((item) => item.id !== id);

  history = history.filter(
    (item) => item.subjectName !== subject.name
  );

  saveData();
  renderAll();

  showToast("Subject deleted.");
}


// 10. PLANNER SUBJECT DROPDOWN

function renderPlannerOptions() {
  const select = $("plannerSubject");
  const previousValue = select.value;

  select.replaceChildren();

  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = "Select a subject";

  select.appendChild(placeholder);

  subjects.forEach((subject) => {
    const option = document.createElement("option");
    option.value = subject.id;
    option.textContent = subject.name;
    select.appendChild(option);
  });

  if (subjects.some((subject) => subject.id === previousValue)) {
    select.value = previousValue;
  }
}


// 11. ATTENDANCE CALCULATOR

function calculateAttendance() {
  const id = $("plannerSubject").value;
  const subject = subjects.find((item) => item.id === id);

  const requestedTarget = Number($("plannerTarget").value);
  const future = Number($("futureClasses").value);

  if (!subject) {
    showToast("Select a subject first.");
    return;
  }

  if (
    !Number.isFinite(requestedTarget) ||
    requestedTarget < 1 ||
    requestedTarget > 100
  ) {
    showToast("Target must be between 1% and 100%.");
    return;
  }

  if (
    !Number.isSafeInteger(future) ||
    future < 0 ||
    future > 10000
  ) {
    showToast("Enter a valid number of upcoming classes.");
    return;
  }

  const attended = subject.attended;
  const total = getTotalClasses(subject);
  const current = total > 0 ? (attended / total) * 100 : 0;
  const required = requestedTarget / 100;

  // If all future classes are attended, this is the projected result.
  const projected = total + future > 0
    ? ((attended + future) / (total + future)) * 100
    : 0;

  // Minimum future classes that must be attended
  // to reach the target within the specified horizon.
  const needed = Math.max(
    0,
    Math.ceil(required * (total + future) - attended - 1e-10)
  );

  const canReach = needed <= future;

  const classesToAttend = Math.min(future, needed);
  const classesCanMiss = canReach ? future - needed : 0;

  // Calculate how many consecutive classes are required
  // if the student attends every class until reaching target.
  let consecutiveNeeded = 0;

  if (current < requestedTarget) {
    if (required === 1) {
      consecutiveNeeded = attended === total ? 0 : Infinity;
    } else {
      consecutiveNeeded = Math.max(
        0,
        Math.ceil(
          (required * total - attended) / (1 - required) - 1e-10
        )
      );
    }
  }

  $("plannerPlaceholder").classList.add("hidden");
  $("plannerOutput").classList.remove("hidden");

  $("forecastPercentage").textContent =
    formatPercentage(projected);

  $("forecastCurrent").textContent =
    formatPercentage(current);

  $("forecastLabel").textContent =
    future === 0
      ? "CURRENT ATTENDANCE"
      : "IF YOU ATTEND ALL UPCOMING CLASSES";

  $("forecastAttend").textContent = canReach
    ? classesToAttend
    : "All " + future;

  $("forecastSkip").textContent = canReach
    ? classesCanMiss
    : "0";

  const title = $("plannerResultTitle");
  const message = $("forecastMessage");

  if (current >= requestedTarget) {
    title.textContent = "You're above your target.";

    if (future === 0) {
      message.textContent =
        `You are currently meeting your ${requestedTarget}% target.`;
    } else {
      message.textContent =
        `You can miss up to ${classesCanMiss} of the next ${future} classes and still remain at or above ${requestedTarget}%.`;
    }

  } else if (canReach) {
    title.textContent = "You can recover your attendance.";

    message.textContent =
      `Attend at least ${classesToAttend} of the next ${future} classes to reach ${requestedTarget}%. You can miss ${classesCanMiss} at most.`;

  } else {
    title.textContent = "You need more classes to recover.";

    message.textContent =
      `Even if you attend all ${future} upcoming classes, your attendance will be ${formatPercentage(projected)}. You need approximately ${consecutiveNeeded} consecutive attended classes from now to reach ${requestedTarget}%.`;
  }

  if (future === 0 && current < requestedTarget) {
    message.textContent =
      `You are currently below ${requestedTarget}%. Attend approximately ${consecutiveNeeded} consecutive classes to reach your target.`;
  }
}


// 12. CLASS HISTORY TABLE

function renderHistory() {
  const tbody = $("historyTableBody");

  tbody.replaceChildren();

  if (history.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");

    cell.colSpan = 4;
    cell.className = "empty-table";
    cell.textContent = "No attendance activity recorded yet.";

    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  history.slice(0, 30).forEach((item) => {
    const row = document.createElement("tr");

    const name = document.createElement("td");
    name.textContent = item.subjectName;

    const date = document.createElement("td");

    const parsedDate = new Date(item.date);

    date.textContent = Number.isNaN(parsedDate.getTime())
      ? "Unknown date"
      : parsedDate.toLocaleString("en-IN", {
          day: "numeric",
          month: "short",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit"
        });

    const status = document.createElement("td");
    status.textContent = item.status;

    if (item.status === "Attended") {
      status.style.color = "var(--green)";
    } else if (item.status === "Missed") {
      status.style.color = "var(--red)";
    }

    const count = document.createElement("td");
    count.textContent = item.count ?? 1;

    row.append(name, date, status, count);
    tbody.appendChild(row);
  });
}


// 13. DEFAULT ATTENDANCE TARGET

function saveTarget() {
  const value = Number($("defaultTarget").value);

  if (
    !Number.isFinite(value) ||
    value < 1 ||
    value > 100
  ) {
    showToast("Enter a target between 1 and 100.");
    return;
  }

  target = value;

  $("plannerTarget").value = target;

  saveData();
  renderAll();

  showToast(`Default target updated to ${target}%.`);
}


// 14. EXPORT DATA

function exportData() {
  const data = {
    app: "AttendIQ",
    version: 1,
    exportedAt: new Date().toISOString(),
    target,
    subjects,
    history
  };

  const blob = new Blob(
    [JSON.stringify(data, null, 2)],
    { type: "application/json" }
  );

  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = "attendiq-backup.json";

  document.body.appendChild(link);
  link.click();
  link.remove();

  URL.revokeObjectURL(url);

  showToast("Attendance backup exported.");
}


// 15. IMPORT DATA

function importData(file) {
  const reader = new FileReader();

  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result);

      if (
        data.app !== "AttendIQ" ||
        !Array.isArray(data.subjects) ||
        !Array.isArray(data.history) ||
        !Number.isFinite(data.target) ||
        data.target < 1 ||
        data.target > 100
      ) {
        throw new Error("Invalid AttendIQ backup.");
      }

      const validSubjects = data.subjects.every((subject) =>
        subject &&
        typeof subject.id === "string" &&
        typeof subject.name === "string" &&
        Number.isSafeInteger(subject.attended) &&
        Number.isSafeInteger(subject.missed) &&
        subject.attended >= 0 &&
        subject.missed >= 0
      );

      const validHistory = data.history.every((item) =>
        item &&
        typeof item.subjectName === "string" &&
        typeof item.date === "string" &&
        ["Attended", "Missed", "Initial record"].includes(item.status)
      );

      if (!validSubjects || !validHistory) {
        throw new Error("Backup contains invalid records.");
      }

      const confirmed = window.confirm(
        "Import this backup? Your current AttendIQ data will be replaced."
      );

      if (!confirmed) return;

      subjects = data.subjects;
      history = data.history.slice(0, 100);
      target = data.target;

      saveData();
      renderAll();

      $("plannerTarget").value = target;

      showToast("Backup imported successfully.");

    } catch (error) {
      console.error(error);
      showToast("Invalid or damaged backup file.");
    }
  };

  reader.onerror = () => {
    showToast("Could not read backup file.");
  };

  reader.readAsText(file);
}


// 16. CLEAR HISTORY

function clearHistory() {
  if (history.length === 0) {
    showToast("History is already empty.");
    return;
  }

  const confirmed = window.confirm(
    "Clear the class activity history? Subject attendance totals will remain unchanged."
  );

  if (!confirmed) return;

  history = [];

  saveData();
  renderHistory();

  showToast("Class history cleared.");
}


// 17. RENDER EVERYTHING

function renderAll() {
  renderOverview();
  renderSubjects();
  renderPlannerOptions();
  renderHistory();
}


// 18. NAVIGATION

function setupNavigation() {
  const links = document.querySelectorAll(".nav-link");

  links.forEach((link) => {
    link.addEventListener("click", () => {
      links.forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
    });
  });
}


// 19. EVENT LISTENERS

function setupEvents() {
  $("addSubjectButton").addEventListener("click", () => {
    openSubjectForm();
  });

  $("subjectAddButton").addEventListener("click", () => {
    openSubjectForm();
  });

  $("emptyAddButton").addEventListener("click", () => {
    openSubjectForm();
  });

  $("subjectForm").addEventListener("submit", handleSubjectSubmit);

  $("closeSubjectForm").addEventListener("click", closeSubjectForm);
  $("cancelSubject").addEventListener("click", closeSubjectForm);

  $("subjectFilter").addEventListener("change", renderSubjects);

  $("calculateButton").addEventListener("click", calculateAttendance);

  $("saveTargetButton").addEventListener("click", saveTarget);

  $("exportButton").addEventListener("click", exportData);

  $("clearHistoryButton").addEventListener("click", clearHistory);

  // Import a backup through a file picker.
  const importButton = document.createElement("button");

  importButton.className = "secondary-button";
  importButton.textContent = "↑ Import backup";
  importButton.type = "button";

  $("exportButton").after(importButton);

  const fileInput = document.createElement("input");

  fileInput.type = "file";
  fileInput.accept = ".json,application/json";
  fileInput.hidden = true;

  document.body.appendChild(fileInput);

  importButton.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    if (file) {
      importData(file);
    }

    fileInput.value = "";
  });

  setupNavigation();
}


// 20. START APPLICATION

function initialize() {
  loadData();
  renderDate();

  $("defaultTarget").value = target;
  $("plannerTarget").value = target;

  setupEvents();
  renderAll();
}

initialize();
