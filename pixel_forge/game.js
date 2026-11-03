
const canvas = document.getElementById("pixelCanvas");
const ctx = canvas.getContext("2d");

const colorPicker = document.getElementById("colorPicker");
const gridSizeSelect = document.getElementById("gridSize");

const pixelCount = document.getElementById("pixelCount");
const activeToolLabel = document.getElementById("activeTool");
const activeColorLabel = document.getElementById("activeColor");
const gridLabel = document.getElementById("gridLabel");

const undoBtn = document.getElementById("undoBtn");
const redoBtn = document.getElementById("redoBtn");
const clearBtn = document.getElementById("clearBtn");
const exportBtn = document.getElementById("exportBtn");

let gridSize = 32;
let currentColor = "#ff6b6b";
let currentTool = "draw";
let isDrawing = false;

let pixels = createGrid(gridSize);
let undoStack = [];
let redoStack = [];

const EMPTY = null;

function createGrid(size) {
  return Array.from(
    { length: size },
    () => Array(size).fill(EMPTY)
  );
}

function saveHistory() {
  undoStack.push(pixels.map(row => [...row]));

  if (undoStack.length > 50) {
    undoStack.shift();
  }

  redoStack = [];
  updateHistoryButtons();
}

function updateHistoryButtons() {
  undoBtn.disabled = undoStack.length === 0;
  redoBtn.disabled = redoStack.length === 0;

  undoBtn.style.opacity = undoBtn.disabled ? "0.4" : "1";
  redoBtn.style.opacity = redoBtn.disabled ? "0.4" : "1";
}

function drawCanvas() {
  const cellSize = canvas.width / gridSize;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw checkerboard background.
  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      ctx.fillStyle = (x + y) % 2 === 0
        ? "#e4e4e4"
        : "#cccccc";

      ctx.fillRect(
        x * cellSize,
        y * cellSize,
        cellSize,
        cellSize
      );

      if (pixels[y][x]) {
        ctx.fillStyle = pixels[y][x];

        ctx.fillRect(
          x * cellSize,
          y * cellSize,
          cellSize,
          cellSize
        );
      }
    }
  }

  // Draw grid lines.
  ctx.strokeStyle = "#00000018";
  ctx.lineWidth = 1;

  for (let i = 0; i <= gridSize; i++) {
    const position = i * cellSize;

    ctx.beginPath();
    ctx.moveTo(position, 0);
    ctx.lineTo(position, canvas.height);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, position);
    ctx.lineTo(canvas.width, position);
    ctx.stroke();
  }

  updatePixelCount();
}

function updatePixelCount() {
  const count = pixels.flat().filter(Boolean).length;
  pixelCount.textContent = `${count} pixels`;
}

function getCell(event) {
  const rect = canvas.getBoundingClientRect();

  const x = Math.floor(
    ((event.clientX - rect.left) / rect.width) * gridSize
  );

  const y = Math.floor(
    ((event.clientY - rect.top) / rect.height) * gridSize
  );

  if (
    x < 0 || x >= gridSize ||
    y < 0 || y >= gridSize
  ) {
    return null;
  }

  return { x, y };
}

function paintCell(x, y) {
  if (currentTool === "draw") {
    pixels[y][x] = currentColor;
  }

  if (currentTool === "eraser") {
    pixels[y][x] = EMPTY;
  }

  drawCanvas();
}

function floodFill(startX, startY) {
  const targetColor = pixels[startY][startX];

  if (targetColor === currentColor) return;

  const stack = [[startX, startY]];

  while (stack.length > 0) {
    const [x, y] = stack.pop();

    if (
      x < 0 || x >= gridSize ||
      y < 0 || y >= gridSize
    ) {
      continue;
    }

    if (pixels[y][x] !== targetColor) {
      continue;
    }

    pixels[y][x] = currentColor;

    stack.push([x + 1, y]);
    stack.push([x - 1, y]);
    stack.push([x, y + 1]);
    stack.push([x, y - 1]);
  }
}

function handlePointerDown(event) {
  event.preventDefault();

  const cell = getCell(event);
  if (!cell) return;

  if (currentTool === "fill") {
    saveHistory();
    floodFill(cell.x, cell.y);
    drawCanvas();
    return;
  }

  saveHistory();
  isDrawing = true;

  canvas.setPointerCapture(event.pointerId);
  paintCell(cell.x, cell.y);
}

function handlePointerMove(event) {
  if (!isDrawing) return;

  const cell = getCell(event);
  if (!cell) return;

  paintCell(cell.x, cell.y);
}

function stopDrawing() {
  isDrawing = false;
}

canvas.addEventListener("pointerdown", handlePointerDown);
canvas.addEventListener("pointermove", handlePointerMove);
canvas.addEventListener("pointerup", stopDrawing);
canvas.addEventListener("pointercancel", stopDrawing);
canvas.addEventListener("lostpointercapture", stopDrawing);

// Tool selection.
document.querySelectorAll(".tool").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tool").forEach(tool => {
      tool.classList.remove("active");
    });

    button.classList.add("active");

    currentTool = button.dataset.tool;

    activeToolLabel.textContent =
      currentTool.charAt(0).toUpperCase() +
      currentTool.slice(1);

    canvas.style.cursor =
      currentTool === "fill" ? "cell" : "crosshair";
  });
});

// Color picker.
colorPicker.addEventListener("input", event => {
  currentColor = event.target.value;
  updateColorLabel();
});

function updateColorLabel() {
  activeColorLabel.textContent = currentColor.toUpperCase();
}

// Preset palette.
document.querySelectorAll("#palette button").forEach(button => {
  button.addEventListener("click", () => {
    currentColor = button.dataset.color;
    colorPicker.value = currentColor;
    updateColorLabel();
  });
});

// Grid size.
gridSizeSelect.addEventListener("change", () => {
  const newSize = Number(gridSizeSelect.value);

  if (newSize === gridSize) return;

  const confirmed = confirm(
    "Changing the canvas size will clear your current artwork. Continue?"
  );

  if (!confirmed) {
    gridSizeSelect.value = String(gridSize);
    return;
  }

  gridSize = newSize;
  pixels = createGrid(gridSize);

  undoStack = [];
  redoStack = [];

  gridLabel.textContent = `${gridSize} × ${gridSize}`;

  updateHistoryButtons();
  drawCanvas();
  saveArtwork();
});

// Undo.
undoBtn.addEventListener("click", () => {
  if (undoStack.length === 0) return;

  redoStack.push(pixels.map(row => [...row]));
  pixels = undoStack.pop();

  updateHistoryButtons();
  drawCanvas();
  saveArtwork();
});

// Redo.
redoBtn.addEventListener("click", () => {
  if (redoStack.length === 0) return;

  undoStack.push(pixels.map(row => [...row]));
  pixels = redoStack.pop();

  updateHistoryButtons();
  drawCanvas();
  saveArtwork();
});

// Clear canvas.
clearBtn.addEventListener("click", () => {
  const hasArtwork = pixels.flat().some(Boolean);

  if (!hasArtwork) return;

  if (!confirm("Clear your entire artwork?")) return;

  saveHistory();
  pixels = createGrid(gridSize);

  drawCanvas();
  saveArtwork();
});

// Export as PNG without grid lines.
exportBtn.addEventListener("click", () => {
  const exportCanvas = document.createElement("canvas");

  exportCanvas.width = gridSize * 16;
  exportCanvas.height = gridSize * 16;

  const exportCtx = exportCanvas.getContext("2d");
  const cellSize = 16;

  exportCtx.clearRect(
    0,
    0,
    exportCanvas.width,
    exportCanvas.height
  );

  for (let y = 0; y < gridSize; y++) {
    for (let x = 0; x < gridSize; x++) {
      if (!pixels[y][x]) continue;

      exportCtx.fillStyle = pixels[y][x];

      exportCtx.fillRect(
        x * cellSize,
        y * cellSize,
        cellSize,
        cellSize
      );
    }
  }

  const link = document.createElement("a");
  link.download = "pixel-forge-artwork.png";
  link.href = exportCanvas.toDataURL("image/png");
  link.click();
});

// Save artwork in browser storage.
function saveArtwork() {
  try {
    localStorage.setItem(
      "pixelForgeArtwork",
      JSON.stringify({
        gridSize,
        pixels
      })
    );
  } catch (error) {
    console.warn("Could not save artwork:", error);
  }
}

function loadArtwork() {
  try {
    const saved = localStorage.getItem("pixelForgeArtwork");

    if (!saved) return;

    const artwork = JSON.parse(saved);

    if (
      !artwork ||
      ![16, 24, 32, 48].includes(artwork.gridSize) ||
      !Array.isArray(artwork.pixels) ||
      artwork.pixels.length !== artwork.gridSize ||
      !artwork.pixels.every(
        row => Array.isArray(row) &&
          row.length === artwork.gridSize
      )
    ) {
      return;
    }

    gridSize = artwork.gridSize;
    pixels = artwork.pixels;

    gridSizeSelect.value = String(gridSize);
    gridLabel.textContent = `${gridSize} × ${gridSize}`;
  } catch (error) {
    console.warn("Could not load saved artwork:", error);
  }
}

// Save after drawing ends.
canvas.addEventListener("pointerup", saveArtwork);
canvas.addEventListener("pointercancel", saveArtwork);
canvas.addEventListener("lostpointercapture", saveArtwork);

// Initial setup.
loadArtwork();
updateColorLabel();
updateHistoryButtons();
drawCanvas();
