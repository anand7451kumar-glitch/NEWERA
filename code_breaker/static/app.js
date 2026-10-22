const L = window.CODE_LENGTH, MAX = window.MAX_ATTEMPTS;
let current = [], state = null;
const $ = (id) => document.getElementById(id);
const say = (t) => ($("message").textContent = t);

async function api(path, body) {
  const res = await fetch(path, body === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}

function dots(colors) {
  return Array.from({ length: L }, (_, i) => `<span class="dot ${colors[i] || ""}"></span>`).join("");
}

function render() {
  const rows = state.guesses.map((g) => {
    const hints = "<span class='hint exact'></span>".repeat(g.exact) + "<span class='hint misplaced'></span>".repeat(g.misplaced);
    return `<div class="row"><div class="pegs">${dots(g.guess)}</div><div class="hints">${hints}</div></div>`;
  });
  for (let i = state.guesses.length; i < MAX; i++) rows.push(`<div class="row empty"><div class="pegs">${dots([])}</div></div>`);
  $("board").innerHTML = rows.join("");
  $("slots").innerHTML = dots(current);
  $("submit").disabled = state.over || current.length !== L;
  $("undo").disabled = state.over || current.length === 0;
  document.querySelectorAll(".peg").forEach((p) => (p.disabled = state.over));
  if (state.won) say(`Cracked it in ${state.guesses.length} ${state.guesses.length === 1 ? "try" : "tries"}!`);
  else if (state.over) say(`Out of tries. The code was ${state.secret.join(", ")}.`);
}

document.querySelectorAll(".peg").forEach((p) =>
  p.addEventListener("click", () => {
    if (current.length < L) { current.push(p.dataset.color); say(""); render(); }
  }));
$("undo").onclick = () => { current.pop(); render(); };
$("submit").onclick = async () => {
  try { state = await api("/api/guess", { guess: current }); current = []; say(""); render(); }
  catch (e) { say(e.message); }
};
$("new").onclick = async () => { state = await api("/api/new", {}); current = []; say(""); render(); };

api("/api/state").then((s) => { state = s; render(); });
