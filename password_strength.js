function checkPassword(password) {
    let score = 0;

    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score ++;
    if (/[!@#$%^&*]/.test(password)) score++;

    if (score <= 1) return "Weak";
    if (score <= 3) return "Medium";
    return "Strong";
}

const password = "!1234567QWERTYUIZXCVBNM1";

console.log("Password strength:", checkPassword(password));
