const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const scoreElement = document.getElementById("score");
const healthElement = document.getElementById("health");
const waveElement = document.getElementById("wave");
const overlay = document.getElementById("overlay");
const message = document.getElementById("message");
const startButton = document.getElementById("start");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;

let player;
let enemies = [];
let orbs = [];

let score = 0;
let health = 3;
let wave = 1;

// Persistent high score
let highScore = Number(localStorage.getItem("neonSurvivorHighScore")) || 0;

let running = false;
let paused = false;
let gameOver = false;

let keys = {};
let lastTime = 0;
let spawnTimer = 0;
let orbTimer = 0;
let animationId = null;

function resetGame() {
    player = {
        x: WIDTH / 2,
        y: HEIGHT / 2,
        radius: 12,
        speed: 250,
        invincible: 0
    };

    enemies = [];
    orbs = [];

    score = 0;
    health = 3;
    wave = 1;

    spawnTimer = 0;
    orbTimer = 0;
    keys = {};

    updateStats();
}

function updateStats() {
    scoreElement.textContent = Math.floor(score);
    healthElement.textContent = health;
    waveElement.textContent = wave;

    // Show the high score in the browser tab title.
    document.title = `Neon Survivor | Best: ${highScore}`;
}

function saveHighScore() {
    if (score > highScore) {
        highScore = Math.floor(score);
        localStorage.setItem("neonSurvivorHighScore", highScore);
    }
}

function startGame() {
    cancelAnimationFrame(animationId);

    resetGame();

    running = true;
    paused = false;
    gameOver = false;

    message.textContent = "READY TO SURVIVE?";
    startButton.textContent = "START GAME";
    overlay.classList.add("hidden");

    lastTime = performance.now();
    animationId = requestAnimationFrame(gameLoop);
}

function endGame() {
    running = false;
    gameOver = true;

    saveHighScore();
    updateStats();

    message.textContent =
        `GAME OVER — SCORE: ${Math.floor(score)} | BEST: ${highScore}`;

    startButton.textContent = "PLAY AGAIN";
    overlay.classList.remove("hidden");
}

function togglePause() {
    if (!running && !paused) return;

    paused = !paused;

    if (paused) {
        running = false;
        message.textContent = "PAUSED";
        startButton.textContent = "RESUME";
        overlay.classList.remove("hidden");
    } else {
        running = true;
        overlay.classList.add("hidden");

        lastTime = performance.now();
        animationId = requestAnimationFrame(gameLoop);
    }
}

function spawnEnemy() {
    const side = Math.floor(Math.random() * 4);

    let x;
    let y;

    if (side === 0) {
        x = 0;
        y = Math.random() * HEIGHT;
    } else if (side === 1) {
        x = WIDTH;
        y = Math.random() * HEIGHT;
    } else if (side === 2) {
        x = Math.random() * WIDTH;
        y = 0;
    } else {
        x = Math.random() * WIDTH;
        y = HEIGHT;
    }

    // Choose enemy type based on the current wave.
    const roll = Math.random();
    let enemy;

    if (wave >= 3 && roll < 0.2) {
        // Tank: large, slow, and takes three hits.
        enemy = {
            x,
            y,
            radius: 17,
            speed: 35 + wave * 3,
            type: "tank",
            hp: 3,
            damageTimer: 0
        };
    } else if (wave >= 2 && roll < 0.5) {
        // Fast enemy: small and difficult to dodge.
        enemy = {
            x,
            y,
            radius: 7,
            speed: 100 + wave * 8,
            type: "fast",
            hp: 1,
            damageTimer: 0
        };
    } else {
        // Normal enemy.
        enemy = {
            x,
            y,
            radius: 10,
            speed: 55 + wave * 9,
            type: "normal",
            hp: 1,
            damageTimer: 0
        };
    }

    enemies.push(enemy);
}

function spawnOrb() {
    orbs.push({
        x: 25 + Math.random() * (WIDTH - 50),
        y: 25 + Math.random() * (HEIGHT - 50),
        radius: 7
    });
}

function distance(a, b) {
    return Math.hypot(a.x - b.x, a.y - b.y);
}

function update(deltaTime) {
    score += deltaTime * 5;
    wave = 1 + Math.floor(score / 100);

    player.invincible = Math.max(
        0,
        player.invincible - deltaTime
    );

    let dx = 0;
    let dy = 0;

    if (keys.ArrowLeft || keys.a) dx--;
    if (keys.ArrowRight || keys.d) dx++;
    if (keys.ArrowUp || keys.w) dy--;
    if (keys.ArrowDown || keys.s) dy++;

    const magnitude = Math.hypot(dx, dy);

    if (magnitude > 0) {
        dx /= magnitude;
        dy /= magnitude;
    }

    player.x += dx * player.speed * deltaTime;
    player.y += dy * player.speed * deltaTime;

    player.x = Math.max(
        player.radius,
        Math.min(WIDTH - player.radius, player.x)
    );

    player.y = Math.max(
        player.radius,
        Math.min(HEIGHT - player.radius, player.y)
    );

    spawnTimer += deltaTime;
    orbTimer += deltaTime;

    const spawnInterval = Math.max(0.3, 1.2 - wave * 0.06);

    if (spawnTimer >= spawnInterval) {
        spawnEnemy();
        spawnTimer = 0;
    }

    if (orbTimer >= 4) {
        spawnOrb();
        orbTimer = 0;
    }

    for (const enemy of enemies) {
        const d = distance(player, enemy);

        if (d > 0) {
            enemy.x +=
                ((player.x - enemy.x) / d) *
                enemy.speed *
                deltaTime;

            enemy.y +=
                ((player.y - enemy.y) / d) *
                enemy.speed *
                deltaTime;
        }

        if (
            d < player.radius + enemy.radius &&
            player.invincible <= 0
        ) {
            health--;
            player.invincible = 1.2;

            updateStats();

            if (health <= 0) {
                endGame();
                return;
            }
        }
    }

    enemies = enemies.filter(enemy =>
        enemy.x > -30 &&
        enemy.x < WIDTH + 30 &&
        enemy.y > -30 &&
        enemy.y < HEIGHT + 30
    );

    orbs = orbs.filter(orb => {
        if (
            distance(player, orb) <
            player.radius + orb.radius
        ) {
            score += 25;
            return false;
        }

        return true;
    });

    updateStats();
}

function draw() {
    ctx.fillStyle = "#080d19";
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // Background grid
    ctx.strokeStyle = "#142238";
    ctx.lineWidth = 1;

    for (let x = 0; x < WIDTH; x += 40) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, HEIGHT);
        ctx.stroke();
    }

    for (let y = 0; y < HEIGHT; y += 40) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(WIDTH, y);
        ctx.stroke();
    }

    // Energy orbs
    for (const orb of orbs) {
        ctx.beginPath();
        ctx.arc(orb.x, orb.y, orb.radius, 0, Math.PI * 2);

        ctx.fillStyle = "#52f1ff";
        ctx.shadowColor = "#52f1ff";
        ctx.shadowBlur = 15;
        ctx.fill();

        ctx.shadowBlur = 0;
    }

    // Enemies
    for (const enemy of enemies) {
        ctx.beginPath();
        ctx.arc(
            enemy.x,
            enemy.y,
            enemy.radius,
            0,
            Math.PI * 2
        );

        if (enemy.type === "tank") {
            ctx.fillStyle = "#a855f7";
            ctx.shadowColor = "#a855f7";
        } else if (enemy.type === "fast") {
            ctx.fillStyle = "#ff9f43";
            ctx.shadowColor = "#ff9f43";
        } else {
            ctx.fillStyle = "#ff426d";
            ctx.shadowColor = "#ff426d";
        }

        ctx.shadowBlur = 12;
        ctx.fill();
        ctx.shadowBlur = 0;

        // Display tank health.
        if (enemy.type === "tank") {
            ctx.fillStyle = "#ffffff";
            ctx.font = "11px Arial";
            ctx.textAlign = "center";
            ctx.fillText(
                enemy.hp,
                enemy.x,
                enemy.y + 4
            );
        }
    }

    // Player
    if (player) {
        ctx.beginPath();
        ctx.arc(
            player.x,
            player.y,
            player.radius,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            player.invincible > 0 &&
            Math.floor(performance.now() / 100) % 2
                ? "#ffffff"
                : "#5ee7f7";

        ctx.shadowColor = "#5ee7f7";
        ctx.shadowBlur = 18;
        ctx.fill();
        ctx.shadowBlur = 0;
    }

    // High score display
    ctx.fillStyle = "#8da4bf";
    ctx.font = "14px Arial";
    ctx.textAlign = "right";
    ctx.fillText(`BEST: ${highScore}`, WIDTH - 15, 25);
}

function gameLoop(timestamp) {
    if (!running || paused) return;

    const deltaTime = Math.min(
        (timestamp - lastTime) / 1000,
        0.04
    );

    lastTime = timestamp;

    update(deltaTime);
    draw();

    if (running) {
        animationId = requestAnimationFrame(gameLoop);
    }
}

document.addEventListener("keydown", event => {
    if (
        ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "]
            .includes(event.key)
    ) {
        event.preventDefault();
    }

    keys[event.key] = true;
    keys[event.key.toLowerCase()] = true;

    if (event.key.toLowerCase() === "p") {
        togglePause();
    }
});

document.addEventListener("keyup", event => {
    keys[event.key] = false;
    keys[event.key.toLowerCase()] = false;
});

startButton.addEventListener("click", () => {
    if (paused && !gameOver) {
        togglePause();
    } else {
        startGame();
    }
});

resetGame();
draw();