
const $ = id => document.getElementById(id);

const clues = {
  clock: {
    name: "The Broken Clock",
    icon: "🕰️",
    description: "The wall clock stopped at 23:47. Its battery is missing. However, the internal mechanism is still working. Someone deliberately stopped it.",
    extra: "FORENSIC NOTE: The clock was manually altered.",
    category: "PHYSICAL EVIDENCE"
  },
  letter: {
    name: "The Unsent Letter",
    icon: "📄",
    description: "A handwritten note on the desk reads: 'If the experiment works, none of this will matter. If it fails, find the original.'",
    extra: "HANDWRITING: Confirmed as Dr. Voss.",
    category: "DOCUMENT EVIDENCE"
  },
  cup: {
    name: "The Coffee Cup",
    icon: "☕",
    description: "Two coffee cups were found. One contains traces of a sedative. The second has no detectable residue.",
    extra: "LAB RESULT: Sedative detected in one cup.",
    category: "FORENSIC EVIDENCE"
  },
  window: {
    name: "The Open Window",
    icon: "🪟",
    description: "The window was open, but the dust on the outside ledge is undisturbed. No one climbed in or out this way.",
    extra: "FORENSIC NOTE: The window is a misleading exit.",
    category: "SCENE EVIDENCE"
  },
  footprint: {
    name: "The Second Footprint",
    icon: "👣",
    description: "A muddy footprint was found near the desk. It is a size 9 shoe, and the soil contains a rare mineral found near the old research facility.",
    extra: "TRACE ANALYSIS: Mineral matches the research facility.",
    category: "TRACE EVIDENCE"
  }
};

const suspects = [
  {
    id: "mara",
    name: "Mara Voss",
    role: "Wife · 42",
    icon: "👩",
    description: "She claims she was at home all evening. She says the doctor had been increasingly paranoid.",
    statements: [
      {
        question: "When did you last see Elias?",
        answer: "Around 22:15. He was working in his study. I went home shortly after."
      },
      {
        question: "Did you know about his experiment?",
        answer: "He told me almost nothing. He said it was dangerous and needed to remain secret."
      },
      {
        question: "Why was your fingerprint on the coffee cup?",
        answer: "I made the coffee. He asked me to bring two cups earlier that evening."
      }
    ]
  },
  {
    id: "daniel",
    name: "Daniel Reed",
    role: "Research Assistant · 29",
    icon: "👨‍🔬",
    description: "Worked with Voss at the research facility. He insists he left at 21:30.",
    statements: [
      {
        question: "When did you leave the facility?",
        answer: "21:30. I went straight home. I never visited the apartment."
      },
      {
        question: "Did you know about the experiment?",
        answer: "I helped build the equipment. Elias was convinced he had discovered something impossible."
      },
      {
        question: "Why is your access card missing?",
        answer: "I lost it two days ago. I reported it to security."
      }
    ]
  },
  {
    id: "victor",
    name: "Victor Hale",
    role: "Building Security · 51",
    icon: "🕵️",
    description: "The night security officer. He says nobody entered the building after 22:00.",
    statements: [
      {
        question: "Was anyone seen entering Apartment 09?",
        answer: "No one. The building logs are clean after 22:00."
      },
      {
        question: "Did you check the cameras?",
        answer: "Yes. There is a recording gap between 23:30 and midnight. System malfunction."
      },
      {
        question: "Where were you at 23:47?",
        answer: "At the security desk. I never left my post."
      }
    ]
  }
];

const timelineEvents = [
  { time: "21:30", text: "Daniel claims to have left the research facility." },
  { time: "22:15", text: "Mara says she last saw Elias in his study." },
  { time: "23:30", text: "Building security cameras stop recording." },
  { time: "23:47", text: "The apartment clock is deliberately stopped." },
  { time: "00:00", text: "Security cameras resume recording." }
];

let state = {
  found: [],
  interviewed: [],
  answers: {},
  selectedSuspect: "",
  timelineVerified: false,
  submitted: false
};

let activeModalAction = null;

function save() {
  localStorage.setItem("case-zero-save", JSON.stringify(state));
}

function load() {
  try {
    const saved = JSON.parse(localStorage.getItem("case-zero-save"));
    if (saved) state = { ...state, ...saved };
  } catch (error) {
    console.warn("Could not load case:", error);
  }
}

load();

function openModal(type, icon, title, description, extra, buttonText, callback) {
  $("modalType").textContent = type;
  $("modalIcon").textContent = icon;
  $("modalTitle").textContent = title;
  $("modalDescription").textContent = description;
  $("modalExtra").textContent = extra;
  $("modalAction").textContent = buttonText;
  activeModalAction = callback;
  $("modal").classList.add("open");
}

function closeModal() {
  $("modal").classList.remove("open");
  activeModalAction = null;
}

$("closeModal").addEventListener("click", closeModal);
$("modal").addEventListener("click", e => {
  if (e.target === $("modal")) closeModal();
});

$("modalAction").addEventListener("click", () => {
  if (activeModalAction) activeModalAction();
  else closeModal();
});

function updateProgress() {
  $("clueCount").textContent = `${state.found.length} / 5`;
  $("interviewCount").textContent = `${state.interviewed.length} / 3`;

  const score =
    state.found.length * 10 +
    state.interviewed.length * 10 +
    (state.timelineVerified ? 20 : 0);

  $("progress").textContent = Math.min(100, score) + "%";
}

function collectClue(id) {
  const clue = clues[id];
  if (!clue) return;

  if (state.found.includes(id)) {
    openModal("PREVIOUSLY DISCOVERED", clue.icon, clue.name, clue.description, clue.extra, "CLOSE FILE", closeModal);
    return;
  }

  openModal(
    "NEW EVIDENCE DISCOVERED",
    clue.icon,
    clue.name,
    clue.description,
    clue.extra,
    "ADD TO EVIDENCE",
    () => {
      state.found.push(id);
      save();
      updateProgress();
      renderEvidence();
      closeModal();
    }
  );
}

document.querySelectorAll(".hotspot").forEach(button => {
  button.addEventListener("click", () => collectClue(button.dataset.clue));
});

function renderEvidence() {
  const container = $("evidenceList");
  container.innerHTML = "";

  if (!state.found.length) {
    container.innerHTML = '<p class="muted">No evidence collected yet. Return to the crime scene.</p>';
    return;
  }

  state.found.forEach(id => {
    const clue = clues[id];
    const card = document.createElement("div");
    card.className = "evidence-card";

    const icon = document.createElement("div");
    icon.className = "evidence-icon";
    icon.textContent = clue.icon;

    const info = document.createElement("div");
    const title = document.createElement("h4");
    title.textContent = clue.name;
    const desc = document.createElement("p");
    desc.textContent = clue.description;
    const tag = document.createElement("span");
    tag.className = "evidence-tag";
    tag.textContent = clue.category;

    info.append(title, desc, tag);
    card.append(icon, info);
    container.append(card);
  });
}

function renderSuspects() {
  const container = $("suspectList");
  container.innerHTML = "";

  suspects.forEach(suspect => {
    const card = document.createElement("div");
    card.className = "suspect-card";

    const avatar = document.createElement("div");
    avatar.className = "suspect-avatar";
    avatar.textContent = suspect.icon;

    const info = document.createElement("div");
    const title = document.createElement("h4");
    title.textContent = suspect.name;
    const role = document.createElement("p");
    role.textContent = suspect.role;
    const description = document.createElement("p");
    description.textContent = suspect.description;
    description.style.marginTop = "8px";

    info.append(title, role, description);

    const button = document.createElement("button");
    button.className = "action-btn";
    button.textContent = state.interviewed.includes(suspect.id) ? "REVISIT INTERVIEW" : "BEGIN INTERVIEW";
    button.addEventListener("click", () => interview(suspect.id));

    card.append(avatar, info, button);
    container.append(card);
  });
}

function interview(id) {
  const suspect = suspects.find(s => s.id === id);
  if (!suspect) return;

  let index = state.answers[id] || 0;

  if (index >= suspect.statements.length) {
    openModal("INTERVIEW COMPLETE", suspect.icon, suspect.name, "You have asked all available questions. Review the statements against your evidence.", "", "CLOSE", closeModal);
    return;
  }

  const statement = suspect.statements[index];

  openModal(
    "INTERROGATION · " + suspect.role.toUpperCase(),
    suspect.icon,
    suspect.name,
    statement.question,
    "RESPONSE: " + statement.answer,
    "NEXT QUESTION",
    () => {
      index++;
      state.answers[id] = index;

      if (index >= suspect.statements.length && !state.interviewed.includes(id)) {
        state.interviewed.push(id);
      }

      save();
      updateProgress();
      renderSuspects();
      closeModal();

      if (index < suspect.statements.length) {
        interview(id);
      } else {
        openModal("INTERVIEW COMPLETE", suspect.icon, "Interview concluded", "All three questions have been answered. Compare the testimony with the physical evidence.", "INTERVIEW RECORDED", "CLOSE", closeModal);
      }
    }
  );
}

function renderTimeline() {
  const container = $("timelineList");
  container.innerHTML = "";

  timelineEvents.forEach((event, index) => {
    const row = document.createElement("div");
    row.className = "timeline-item";

    const time = document.createElement("strong");
    time.textContent = event.time;

    const text = document.createElement("span");
    text.textContent = event.text;

    row.append(time, text);
    container.append(row);
  });
}

$("checkTimeline").addEventListener("click", () => {
  if (state.found.length < 3 || state.interviewed.length < 2) {
    $("timelineResult").textContent = "More evidence and interviews are required.";
    return;
  }

  state.timelineVerified = true;
  save();
  updateProgress();

  $("timelineResult").textContent = "✓ Reconstruction accepted. The camera gap and clock discrepancy are now connected.";
});

function renderAccusations() {
  const container = $("accusationOptions");
  container.innerHTML = "";

  suspects.forEach(suspect => {
    const label = document.createElement("label");
    label.className = "accusation-card";

    const input = document.createElement("input");
    input.type = "radio";
    input.name = "suspect";
    input.value = suspect.id;
    input.checked = state.selectedSuspect === suspect.id;

    input.addEventListener("change", () => {
      state.selectedSuspect = suspect.id;
      save();
      renderAccusations();
    });

    const icon = document.createElement("span");
    icon.textContent = suspect.icon;

    const name = document.createElement("strong");
    name.textContent = `${suspect.name} · ${suspect.role}`;

    label.append(input, icon, name);
    if (state.selectedSuspect === suspect.id) label.classList.add("selected");

    container.append(label);
  });
}

$("submitAccusation").addEventListener("click", () => {
  if (state.submitted) {
    openModal("CASE CLOSED", "📁", "Investigation already submitted", "This case has already been concluded. Reset the investigation to start again.", "", "CLOSE", closeModal);
    return;
  }

  if (!state.selectedSuspect) {
    openModal("ACTION REQUIRED", "⚠️", "No suspect selected", "Choose a suspect before submitting your final report.", "", "CLOSE", closeModal);
    return;
  }

  if (state.found.length < 3 || state.interviewed.length < 2) {
    openModal("INCOMPLETE INVESTIGATION", "🔎", "Insufficient evidence", "Collect at least three clues and complete two interviews before making your accusation.", "", "CONTINUE INVESTIGATION", closeModal);
    return;
  }

  const correctSuspect = "daniel";
  const correct = state.selectedSuspect === correctSuspect;
  const fullCase = state.found.length === 5 && state.interviewed.length === 3 && state.timelineVerified;

  let title;
  let description;

  if (correct && fullCase) {
    title = "CASE SOLVED — EXCEPTIONAL";
    description = "You identified Daniel Reed and reconstructed the full timeline. His missing access card, the camera blackout and the mineral traces connect him to the apartment. The investigation reveals that he helped Voss disappear to protect the experiment.";
  } else if (correct) {
    title = "CASE SOLVED";
    description = "You identified Daniel Reed. The evidence points to his involvement, although some details of the disappearance remain unresolved.";
  } else {
    title = "CASE UNRESOLVED";
    description = "Your accusation does not match the investigation's central finding. The evidence was incomplete or misinterpreted. The truth remains hidden.";
  }

  state.submitted = true;
  save();

  $("ending").textContent = title + " — " + description;
  $("ending").classList.add("show");

  openModal(
    correct ? "INVESTIGATION COMPLETE" : "INVESTIGATION REPORT",
    correct ? "✓" : "📁",
    title,
    description,
    fullCase && correct ? "PERFECT INVESTIGATION · ALL CLUES RECOVERED" : "",
    "VIEW FINAL REPORT",
    () => {
      closeModal();
      $("ending").scrollIntoView({ behavior: "smooth", block: "center" });
    }
  );
});

document.querySelectorAll(".tab").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-page").forEach(p => p.classList.remove("active"));

    button.classList.add("active");
    $("page-" + button.dataset.tab).classList.add("active");
  });
});

$("startButton").addEventListener("click", () => {
  document.querySelector(".game").scrollIntoView({ behavior: "smooth" });
});

$("resetButton").addEventListener("click", () => {
  if (!confirm("Reset this investigation? All collected evidence and interviews will be erased.")) return;

  state = {
    found: [],
    interviewed: [],
    answers: {},
    selectedSuspect: "",
    timelineVerified: false,
    submitted: false
  };

  save();
  $("ending").classList.remove("show");
  $("ending").textContent = "";
  $("timelineResult").textContent = "";

  renderEvidence();
  renderSuspects();
  renderTimeline();
  renderAccusations();
  updateProgress();

  document.querySelector('[data-tab="scene"]').click();
  openModal("NEW INVESTIGATION", "📁", "Case reopened", "All investigation records have been cleared. Begin again at Apartment 09.", "", "START", closeModal);
});

function updateClock() {
  const now = new Date();
  $("caseClock").textContent =
    [now.getHours(), now.getMinutes(), now.getSeconds()]
      .map(v => String(v).padStart(2, "0"))
      .join(":");
}

renderEvidence();
renderSuspects();
renderTimeline();
renderAccusations();
updateProgress();
updateClock();
setInterval(updateClock, 1000);

if (state.submitted) {
  $("ending").classList.add("show");
  $("ending").textContent = "A final report has already been submitted. Reset the case to investigate again.";
}
