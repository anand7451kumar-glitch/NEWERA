const tasks = [];

function addTask(task) {
    tasks.push({ task, done: false });
}

function showTasks() {
    tasks.forEach((item, i) => {
        console.log(`${i + 1}. ${item.done ? "✓" : "☐"} ${item.task}`);
    });
}

addTask("Study JavaScript");
addTask("Practice DSA");
addTask("Push code to GitHub");

showTasks();
