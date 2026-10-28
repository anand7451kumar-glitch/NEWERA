const $ = (id) => document.getElementById(id);
const ROWS = 6, COLS = 5, LAYOUT = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];
let run, row, letters, done, busy, keyState;

async function api(path, body) {
  const res = await fetch(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Server error");
  return data;
}
const say = (t) => ($("message").textContent = t);

function buildBoard() {
  $("board").replaceChildren(...Array.from({ length: ROWS }, () => {
    const r = document.createElement("div"); r.className = "row";
    for (let i = 0; i < COLS; i++) r.appendChild(Object.assign(document.createElement("div"), { className: "tile" }));
    return r;
  }));
}

function buildKeys() {
  const rows = LAYOUT.map((letters, i) => {
    const r = document.createElement("div"); r.className = "krow";
    if (i === 2) r.appendChild(makeKey("Enter", "enter", true));
    [...letters].forEach((l) => r.appendChild(makeKey(l, l)));
    if (i === 2) r.appendChild(makeKey("Del", "backspace", true));
    return r;
  });
  $("keys").replaceChildren(...rows);
}
function makeKey(label, key, wide) {
  const b = document.createElement("button");
  b.className = "key" + (wide ? " wide" : ""); b.textContent = label; b.dataset.key = key;
  b.onclick = () => press(key);
  return b;
}

function showRow() {
  const tiles = $("board").children[row].children;
  for (let i = 0; i < COLS; i++) { tiles[i].textContent = letters[i] || ""; tiles[i].classList.toggle("filled", !!letters[i]); }
}

function paintKeys() {
  document.querySelectorAll(".key").forEach((k) => {
    k.classList.remove("s0", "s1", "s2");
    if (keyState[k.dataset.key] !== undefined) k.classList.add("s" + keyState[k.dataset.key]);
  });
}

async function submit() {
  if (letters.length < COLS) { shake(); say("Not enough letters."); return; }
  busy = true;
  try {
    const word = letters.join("");
    const res = await api("/api/guess", { run, word });
    const tiles = $("board").children[row].children;
    res.pattern.forEach((s, i) => {
      tiles[i].classList.add("s" + s, "flip"); tiles[i].style.setProperty("--i", i);
      keyState[word[i]] = Math.max(keyState[word[i]] ?? 0, s);
    });
    paintKeys();
    $("left").textContent = res.remaining;
    if (res.solved) { done = true; say(`Solved in ${row + 1}! That guess gave ${res.bits} bits of information.`); }
    else if (res.over) { done = true; say(`Out of tries. The word was ${res.answer.toUpperCase()}.`); }
    else say(`That guess gave ${res.bits} bits and cut the list to ${res.remaining} words.`);
    row++; letters = [];
  } catch (e) { shake(); say(e.message); }
  busy = false;
}

function shake() { const r = $("board").children[row]; r.classList.remove("shake"); void r.offsetWidth; r.classList.add("shake"); }

function press(key) {
  if (done || busy || !run) return;
  if (key === "enter") submit();
  else if (key === "backspace") { letters.pop(); showRow(); }
  else if (/^[a-z]$/.test(key) && letters.length < COLS) { letters.push(key); say(""); showRow(); }
}

async function coach() {
  if (done || busy) return;
  try {
    const h = await api("/api/hint", { run });
    letters = [...h.word]; showRow();
    say(`Coach suggests "${h.word.toUpperCase()}": about ${h.bits} bits expected from ${h.remaining} possible words. Press Enter to play it.`);
  } catch (e) { say(e.message); }
}

async function newGame() {
  const d = await api("/api/new");
  run = d.run; row = 0; letters = []; done = false; busy = false; keyState = {};
  buildBoard(); paintKeys(); $("left").textContent = d.remaining; say("Type a word and press Enter.");
}

document.addEventListener("keydown", (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const k = e.key.toLowerCase();
  if (k === "enter" && e.target.tagName === "BUTTON") return;
  if (k === "enter" || k === "backspace" || /^[a-z]$/.test(k)) press(k);
});
$("new").onclick = newGame; $("hint").onclick = coach;
buildKeys(); newGame().catch(() => say("Can't reach the server. Is app.py running?"));
