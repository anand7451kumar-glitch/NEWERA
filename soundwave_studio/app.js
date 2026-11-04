
const canvas = document.getElementById("visualizer");
const ctx = canvas.getContext("2d");

const stage = document.getElementById("visualizerStage");
const audioFile = document.getElementById("audioFile");
const audioPlayer = document.getElementById("audioPlayer");

const emptyState = document.getElementById("emptyState");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");

const trackName = document.getElementById("trackName");
const trackStatus = document.getElementById("trackStatus");

const modeTitle = document.getElementById("modeTitle");
const frequencyLabel = document.getElementById("frequencyLabel");

const colorSelect = document.getElementById("colorSelect");
const sensitivity = document.getElementById("sensitivity");
const sensitivityValue = document.getElementById("sensitivityValue");

const micBtn = document.getElementById("micBtn");
const stopBtn = document.getElementById("stopBtn");
const fullscreenBtn = document.getElementById("fullscreenBtn");
const exportBtn = document.getElementById("exportBtn");

let audioContext = null;
let analyser = null;
let dataArray = null;

let fileSource = null;
let microphoneSource = null;
let microphoneStream = null;

let currentMode = "bars";
let currentTheme = "purple";
let currentSensitivity = 1.5;

let animationId = null;
let audioLoaded = false;
let isMicrophoneActive = false;

let canvasWidth = 0;
let canvasHeight = 0;

const themes = {
  purple: ["#a78bfa", "#6d4aff", "#e1d5ff"],
  cyan: ["#35d9ff", "#087cbd", "#b5f5ff"],
  fire: ["#ffb347", "#ff4d4d", "#ffe0a3"],
  green: ["#63f5a6", "#13a66a", "#c0ffdc"],
  rainbow: ["#ff4b91", "#a78bfa", "#35d9ff"]
};

function resizeCanvas() {
  const rect = stage.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 2);

  canvasWidth = rect.width;
  canvasHeight = rect.height;

  canvas.width = Math.floor(canvasWidth * dpr);
  canvas.height = Math.floor(canvasHeight * dpr);

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

  drawIdleBackground();
}

function drawIdleBackground() {
  ctx.clearRect(0, 0, canvasWidth, canvasHeight);

  const gradient = ctx.createRadialGradient(
    canvasWidth / 2,
    canvasHeight / 2,
    10,
    canvasWidth / 2,
    canvasHeight / 2,
    canvasWidth * 0.6
  );

  gradient.addColorStop(0, "#211c38");
  gradient.addColorStop(1, "#10141e");

  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, canvasWidth, canvasHeight);
}

function initializeAudio() {
  if (audioContext) return;

  const AudioContextClass =
    window.AudioContext || window.webkitAudioContext;

  if (!AudioContextClass) {
    throw new Error("Your browser does not support the Web Audio API.");
  }

  audioContext = new AudioContextClass();

  analyser = audioContext.createAnalyser();
  analyser.fftSize = 2048;
  analyser.smoothingTimeConstant = 0.82;

  dataArray = new Uint8Array(analyser.frequencyBinCount);

  analyser.connect(audioContext.destination);
}

async function activateAudio() {
  initializeAudio();

  if (audioContext.state === "suspended") {
    await audioContext.resume();
  }
}

function setStatus(active, message) {
  statusDot.classList.toggle("active", active);
  statusText.textContent = message;
}

function updateEmptyState() {
  emptyState.style.display =
    audioLoaded || isMicrophoneActive ? "none" : "flex";
}

function updateTrackInfo(name, description) {
  trackName.textContent = name;
  trackStatus.textContent = description;
}

// Load audio file.
audioFile.addEventListener("change", async event => {
  const file = event.target.files[0];

  if (!file) return;

  try {
    stopMicrophone();

    const oldUrl = audioPlayer.dataset.objectUrl;

    if (oldUrl) {
      URL.revokeObjectURL(oldUrl);
    }

    const url = URL.createObjectURL(file);

    audioPlayer.src = url;
    audioPlayer.dataset.objectUrl = url;

    audioLoaded = true;

    updateTrackInfo(file.name, "Audio file ready");
    updateEmptyState();

    await activateAudio();

    if (!fileSource) {
      fileSource = audioContext.createMediaElementSource(audioPlayer);
      fileSource.connect(analyser);
    }

    await audioPlayer.play();

    setStatus(true, "PLAYING AUDIO");
    updateTrackInfo(file.name, "Now playing");

    startVisualizer();

  } catch (error) {
    console.error(error);
    setStatus(false, "PLAYBACK ERROR");
    updateTrackInfo(file.name, "Press play to try again");
  }
});

// Audio playback events.
audioPlayer.addEventListener("play", async () => {
  try {
    if (!audioLoaded) return;

    await activateAudio();

    setStatus(true, "PLAYING AUDIO");
    updateEmptyState();
    startVisualizer();
  } catch (error) {
    console.error(error);
    setStatus(false, "AUDIO ERROR");
  }
});

audioPlayer.addEventListener("pause", () => {
  if (!isMicrophoneActive) {
    setStatus(false, "PAUSED");
  }
});

audioPlayer.addEventListener("ended", () => {
  if (!isMicrophoneActive) {
    setStatus(false, "TRACK ENDED");
  }
});

// Microphone.
micBtn.addEventListener("click", async () => {
  if (isMicrophoneActive) {
    stopMicrophone();
    return;
  }

  if (!navigator.mediaDevices?.getUserMedia) {
    alert("Microphone access requires a supported browser and a secure context such as localhost.");
    return;
  }

  try {
    await activateAudio();

    microphoneStream =
      await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: false,
          noiseSuppression: false,
          autoGainControl: false
        }
      });

    microphoneSource =
      audioContext.createMediaStreamSource(microphoneStream);

    microphoneSource.connect(analyser);

    isMicrophoneActive = true;

    micBtn.classList.add("listening");
    micBtn.innerHTML = "● Stop microphone";

    audioLoaded = false;

    audioPlayer.pause();

    updateTrackInfo("Live microphone", "Listening to input");
    updateEmptyState();

    setStatus(true, "MICROPHONE ACTIVE");
    startVisualizer();

  } catch (error) {
    console.error(error);
    setStatus(false, "MICROPHONE ERROR");

    alert(
      "Could not access the microphone. Check your browser's microphone permission."
    );
  }
});

function stopMicrophone() {
  if (microphoneStream) {
    microphoneStream.getTracks().forEach(track => track.stop());
    microphoneStream = null;
  }

  if (microphoneSource) {
    microphoneSource.disconnect();
    microphoneSource = null;
  }

  isMicrophoneActive = false;

  micBtn.classList.remove("listening");
  micBtn.innerHTML = "🎙 Use microphone";

  if (!audioPlayer.paused && audioLoaded) {
    setStatus(true, "PLAYING AUDIO");
  } else {
    setStatus(false, "STANDBY");
  }

  updateEmptyState();
}

stopBtn.addEventListener("click", stopMicrophone);

// Mode selection.
document.querySelectorAll(".mode-btn").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".mode-btn").forEach(item => {
      item.classList.remove("active");
    });

    button.classList.add("active");

    currentMode = button.dataset.mode;

    const names = {
      bars: "Frequency Spectrum",
      wave: "Live Waveform",
      radial: "Radial Spectrum"
    };

    modeTitle.textContent = names[currentMode];
  });
});

// Theme selection.
colorSelect.addEventListener("change", () => {
  currentTheme = colorSelect.value;
});

// Sensitivity.
sensitivity.addEventListener("input", () => {
  currentSensitivity = Number(sensitivity.value);

  sensitivityValue.textContent =
    currentSensitivity.toFixed(1) + "×";
});

function getColor(index, total) {
  const colors = themes[currentTheme];

  if (currentTheme === "rainbow") {
    return `hsl(${(index / total) * 300 + 180}, 90%, 65%)`;
  }

  const ratio = index / Math.max(total - 1, 1);

  if (ratio < 0.5) return colors[0];
  return colors[1];
}

function getFrequency() {
  if (!analyser) return 0;

  analyser.getByteFrequencyData(dataArray);

  let total = 0;

  for (let i = 0; i < dataArray.length; i++) {
    total += dataArray[i];
  }

  return Math.round(total / dataArray.length);
}

function drawBars() {
  analyser.getByteFrequencyData(dataArray);

  const count = 100;
  const gap = 3;
  const barWidth = canvasWidth / count - gap;

  const usableHeight = canvasHeight * 0.72;
  const startY = canvasHeight * 0.88;

  for (let i = 0; i < count; i++) {
    const index = Math.floor(
      Math.pow(i / count, 1.7) * dataArray.length
    );

    const value = dataArray[index] / 255;

    const height = Math.max(
      2,
      value * usableHeight * currentSensitivity
    );

    const x = i * (barWidth + gap);
    const y = startY - height;

    const gradient = ctx.createLinearGradient(
      0, y, 0, startY
    );

    gradient.addColorStop(0, getColor(i, count));
    gradient.addColorStop(1, "#34245c");

    ctx.fillStyle = gradient;

    ctx.shadowBlur = 12;
    ctx.shadowColor = getColor(i, count);

    ctx.beginPath();
    ctx.roundRect(
      x,
      y,
      Math.max(1, barWidth),
      height,
      4
    );
    ctx.fill();
  }

  ctx.shadowBlur = 0;
}

function drawWave() {
  analyser.getByteTimeDomainData(dataArray);

  const middle = canvasHeight / 2;

  ctx.beginPath();

  const gradient = ctx.createLinearGradient(
    0, 0, canvasWidth, 0
  );

  gradient.addColorStop(0, themes[currentTheme][0]);
  gradient.addColorStop(0.5, themes[currentTheme][2]);
  gradient.addColorStop(1, themes[currentTheme][1]);

  ctx.strokeStyle = gradient;
  ctx.lineWidth = 2.5;
  ctx.shadowBlur = 15;
  ctx.shadowColor = themes[currentTheme][0];

  for (let i = 0; i < dataArray.length; i++) {
    const x = (i / dataArray.length) * canvasWidth;

    const value = (dataArray[i] - 128) / 128;

    const y =
      middle + value * middle * 0.85 * currentSensitivity;

    if (i === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  }

  ctx.stroke();
  ctx.shadowBlur = 0;
}

function drawRadial() {
  analyser.getByteFrequencyData(dataArray);

  const centerX = canvasWidth / 2;
  const centerY = canvasHeight / 2;

  const radius = Math.min(canvasWidth, canvasHeight) * 0.19;
  const count = 120;

  for (let i = 0; i < count; i++) {
    const index = Math.floor(
      (i / count) * dataArray.length * 0.8
    );

    const value = dataArray[index] / 255;

    const length =
      value * radius * currentSensitivity * 1.4;

    const angle = (i / count) * Math.PI * 2;

    const x1 = centerX + Math.cos(angle) * radius;
    const y1 = centerY + Math.sin(angle) * radius;

    const x2 = centerX + Math.cos(angle) * (radius + length);
    const y2 = centerY + Math.sin(angle) * (radius + length);

    ctx.strokeStyle = getColor(i, count);
    ctx.lineWidth = 2.5;
    ctx.shadowBlur = 10;
    ctx.shadowColor = getColor(i, count);

    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  ctx.shadowBlur = 0;

  ctx.beginPath();
  ctx.arc(centerX, centerY, radius - 3, 0, Math.PI * 2);

  ctx.strokeStyle = themes[currentTheme][2];
  ctx.lineWidth = 1;
  ctx.stroke();
}

function render() {
  if (!analyser) return;

  animationId = requestAnimationFrame(render);

  ctx.clearRect(0, 0, canvasWidth, canvasHeight);

  const frequency = getFrequency();

  frequencyLabel.textContent = `${frequency} / 255`;

  if (currentMode === "bars") {
    drawBars();
  } else if (currentMode === "wave") {
    drawWave();
  } else if (currentMode === "radial") {
    drawRadial();
  }
}

function startVisualizer() {
  if (animationId) return;

  render();
}

// Fullscreen.
fullscreenBtn.addEventListener("click", async () => {
  try {
    if (!document.fullscreenElement) {
      await stage.requestFullscreen();
    } else {
      await document.exitFullscreen();
    }
  } catch (error) {
    console.error("Fullscreen unavailable:", error);
  }
});

// Export current visualization.
exportBtn.addEventListener("click", () => {
  const link = document.createElement("a");

  link.download = "soundwave-visualization.png";
  link.href = canvas.toDataURL("image/png");

  link.click();
});

// Resize handling.
const resizeObserver = new ResizeObserver(resizeCanvas);
resizeObserver.observe(stage);

window.addEventListener("beforeunload", () => {
  if (microphoneStream) {
    microphoneStream.getTracks().forEach(track => track.stop());
  }

  if (audioPlayer.dataset.objectUrl) {
    URL.revokeObjectURL(audioPlayer.dataset.objectUrl);
  }
});

// Initial setup.
resizeCanvas();
updateEmptyState();
