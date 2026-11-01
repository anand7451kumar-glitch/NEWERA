
"use strict";

// ==========================================
// CASEFILE: THE LAST SIGNAL
// Main game logic
// ==========================================

const $ = (id) => document.getElementById(id);

// ------------------------------------------
// GAME DATA
// ------------------------------------------

const evidence = {
  computer: {
    title: "Research Terminal",
    description:
      "The laboratory computer was left running. A folder named PROJECT ECHO was open. Its last modified time was 11:42 PM, just five minutes before Dr. Voss disappeared.",
    clue:
      "CLUE DISCOVERED: The research data was accessed shortly before the disappearance."
  },

  radio: {
    title: "Radio Receiver",
    description:
      "The receiver contains a recording of a strange repeating signal. The signal was transmitted at 11:47 PM. However, its source appears to be inside the laboratory itself.",
    clue:
      "CLUE DISCOVERED: The mysterious signal was transmitted from inside the facility."
  },

  keycard: {
    title: "Access Keycard",
    description:
      "A damaged access card was found near the laboratory entrance. Its access history shows an entry at 11:46 PM under an employee account.",
    clue:
      "CLUE DISCOVERED: Someone entered the laboratory one minute before the signal."
  },

  coffee: {
    title: "Coffee Cup",
    description:
      "A coffee cup was found beside the research terminal. Laboratory staff confirm that Dr. Voss never drank coffee. A partial fingerprint belongs to someone with access to the facility.",
    clue:
      "CLUE DISCOVERED: Another person was using the research terminal that evening."
  },

  footage: {
    title: "Security Footage",
    description:
      "The footage shows an empty hallway at 11:47 PM. But the recording skips exactly 43 seconds. The system was manually interrupted, not damaged.",
    clue:
      "CLUE DISCOVERED: The security recording was deliberately manipulated."
  }
};

// ------------------------------------------
// GAME STATE
// ------------------------------------------

const state = {
  examined: [],
  selectedEvidence: null,
  startedAt: Date.now(),
  finished: false
};

// ------------------------------------------
// CLOCK
// ------------------------------------------

function updateClock() {
  const elapsed = Math.floor((Date.now() - state.startedAt) / 1000);

  const hours = String(Math.floor(elapsed / 3600)).padStart(2, "0");
  const minutes = String(Math.floor((elapsed % 3600) / 60)).padStart(2, "0");
  const seconds = String(elapsed % 60).padStart(2, "0");

  $("caseClock").textContent = `${hours}:${minutes}:${seconds}`;
}

// ------------------------------------------
// PROGRESS
// ------------------------------------------

function updateProgress() {
  const total = Object.keys(evidence).length;
  const completed = state.examined.length;
  const percentage = Math.round((completed / total) * 100);

  $("progressText").textContent = `${percentage}%`;
  $("progressBar").style.width = `${percentage}%`;

  $("evidenceCounter").textContent =
    `${completed} / ${total} EXAMINED`;

  if (completed === total) {
    $("deductionWarning").textContent =
      "ALL EVIDENCE EXAMINED — YOU MAY NOW SUBMIT YOUR THEORY.";

    $("deductionWarning").style.color = "#8db99b";
    $("deductionWarning").style.borderColor = "#526c57";
  }

  if (completed === total) {
    $("progressText").textContent = "READY";
  }
}

// ------------------------------------------
// EVIDENCE INSPECTION
// ------------------------------------------

function inspectEvidence(id) {
  if (state.finished) return;

  const item = evidence[id];

  if (!item) return;

  state.selectedEvidence = id;

  const card = document.querySelector(
    `[data-evidence="${id}"]`
  );

  const alreadyExamined = state.examined.includes(id);

  if (!alreadyExamined) {
    state.examined.push(id);
    card.classList.add("examined");

    card.querySelector(".evidence-state").textContent =
      "✓ EXAMINED";
  }

  $("inspectionPanel").innerHTML = `
    <div class="inspection-content">
      <span class="evidence-type">EVIDENCE REPORT</span>
      <h4>${item.title}</h4>
      <p>${item.description}</p>
      <div class="clue-found">
        ${item.clue}
      </div>
    </div>
  `;

  updateProgress();
}

// ------------------------------------------
// NAVIGATION
// ------------------------------------------

function showSection(section) {
  const sections = {
    evidence: {
      element: "evidenceSection",
      title: "Evidence Board"
    },
    suspects: {
      element: "suspectsSection",
      title: "Suspect Profiles"
    },
    deduction: {
      element: "deductionSection",
      title: "Final Deduction"
    }
  };

  if (!sections[section]) return;

  Object.values(sections).forEach((item) => {
    $(item.element).classList.add("hidden");
  });

  $(sections[section].element).classList.remove("hidden");

  $("sectionTitle").textContent = sections[section].title;

  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle(
      "active",
      button.dataset.section === section
    );
  });

  if (section === "deduction") {
    $("deductionWarning").textContent =
      state.examined.length === 5
        ? "ALL EVIDENCE EXAMINED — YOU MAY NOW SUBMIT YOUR THEORY."
        : `INVESTIGATION INCOMPLETE — ${5 - state.examined.length} ITEMS REMAINING.`;
  }
}

// ------------------------------------------
// FINAL DEDUCTION
// ------------------------------------------

function submitDeduction() {
  if (state.finished) return;

  const culprit = $("culpritSelect").value;
  const motive = $("motiveSelect").value;
  const method = $("methodSelect").value;

  const result = $("deductionResult");

  if (state.examined.length !== 5) {
    result.classList.remove("hidden");
    result.classList.add("failure");
    result.textContent =
      "You cannot close the case yet. Examine all five pieces of evidence first.";
    return;
  }

  if (!culprit || !motive || !method) {
    result.classList.remove("hidden");
    result.classList.add("failure");
    result.textContent =
      "Your theory is incomplete. Select a suspect, motive and method.";
    return;
  }

  // Fictional solution for this case.
  // The complete solution will be revealed after submission.

  const correct = {
    culprit: "sarah",
    motive: "coverup",
    method: "camera"
  };

  const correctCount = [
    culprit === correct.culprit,
    motive === correct.motive,
    method === correct.method
  ].filter(Boolean).length;

  state.finished = true;

  result.classList.remove("hidden");
  result.classList.remove("failure");

  if (correctCount === 3) {
    result.innerHTML = `
      <strong>CASE CLOSED — PERFECT DEDUCTION</strong>
      <p>
        You identified the correct suspect, motive and method.
        Your investigation was successful.
      </p>
      <p>
        Sarah Chen manipulated the security footage to conceal
        an unauthorized experiment. The radio signal was used
        to create a false timeline.
      </p>
      <p>RANK: MASTER DETECTIVE</p>
      <button class="submit-button" id="restartButton">
        INVESTIGATE AGAIN →
      </button>
    `;
  } else if (correctCount === 2) {
    result.innerHTML = `
      <strong>PARTIAL SUCCESS — TWO CORRECT</strong>
      <p>
        You were close, but one part of your theory was incorrect.
        The case solution is now revealed.
      </p>
      <p>
        Sarah Chen. Motive: cover up an experiment.
        Method: manipulate the security footage.
      </p>
      <p>RANK: FIELD DETECTIVE</p>
      <button class="submit-button" id="restartButton">
        INVESTIGATE AGAIN →
      </button>
    `;
  } else {
    result.classList.add("failure");
    result.innerHTML = `
      <strong>THEORY REJECTED — CASE REVIEW</strong>
      <p>
        Your deduction did not match the evidence.
        The actual solution was Sarah Chen, who covered up
        an experiment by manipulating the security footage.
      </p>
      <p>RANK: TRAINEE DETECTIVE</p>
      <button class="submit-button" id="restartButton">
        TRY ANOTHER CASE →
      </button>
    `;
  }

  $("submitDeduction").disabled = true;

  $("restartButton").addEventListener("click", restartGame);
}

// ------------------------------------------
// RESTART
// ------------------------------------------

function restartGame() {
  state.examined = [];
  state.selectedEvidence = null;
  state.startedAt = Date.now();
  state.finished = false;

  document.querySelectorAll(".evidence-card").forEach((card) => {
    card.classList.remove("examined");

    card.querySelector(".evidence-state").textContent =
      "NOT EXAMINED";
  });

  $("inspectionPanel").innerHTML = `
    <div class="inspection-placeholder">
      <span>◎</span>
      <p>Select an evidence item to begin inspection.</p>
    </div>
  `;

  $("culpritSelect").value = "";
  $("motiveSelect").value = "";
  $("methodSelect").value = "";

  $("deductionResult").classList.add("hidden");
  $("deductionResult").classList.remove("failure");

  $("submitDeduction").disabled = false;

  updateProgress();
  showSection("evidence");
}

// ------------------------------------------
// EVENT LISTENERS
// ------------------------------------------

document.querySelectorAll(".evidence-card").forEach((card) => {
  card.addEventListener("click", () => {
    inspectEvidence(card.dataset.evidence);
  });
});

document.querySelectorAll(".nav-item").forEach((button) => {
  button.addEventListener("click", () => {
    showSection(button.dataset.section);
  });
});

$("submitDeduction").addEventListener("click", submitDeduction);

// ------------------------------------------
// INITIALIZE
// ------------------------------------------

updateProgress();
updateClock();

setInterval(updateClock, 1000);

console.log("CASEFILE SYSTEM INITIALIZED");
console.log("CASE 0471: THE LAST SIGNAL");
