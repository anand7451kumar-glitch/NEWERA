const expenses = [
    {name: "Food", amount: 250, category: "Foof" },
    {name: "Bus", amount: 50, category: "Transport"},
    {name: "Movie", amount: 300, category: "Entertainment"},
    {name: "Lunch", amount: 180, category: "Food" }
];

function totalExpenses(expenses) {
    return expenses.reduce((total, expense) => {
        return total + expense.amount;
    }, 0);
}

function categoryTotal(expenses, category) {
    return expenses
        .filter(expense => expense.category === category)
        .reduce((total, expense) => total + expense.amount, 0);
}

function highestExpense(expenses) {
    return expenses.reduce((highest, expense) => {
        return expense.amount > highest.amount ? expense : highest;
    });
}

console.log("Total spent:", totalExpenses(expenses));

console.log(
    "Food spending:",
    categoryTotal(expenses, "Food")
);

console.log("Highest expense:",
    highestExpense(expenses)
);
