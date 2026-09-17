const readline = require("readline");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%";

rl.question("Password length: ", length => {
    let password = "";

    for (let i = 0; i < Number(length); i++) {
        password += chars[Math.floor(Math.random() * chars.length)];
    }

    console.log("Generated password:", password);
    rl.close();
});
