import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
"""private fun loadExpenses(context: Context): List<Expense> {
    val prefs = context.getSharedPreferences(ExpenseStore, 0)
    if (!prefs.contains("items")) return emptyList()
    val raw = prefs.getString("items", "") ?: ""
    if (raw.isBlank()) return emptyList()
    return raw.lines().mapNotNull { line ->
        val parts = line.split("\\t")
        if (parts.size >= 3) {
            val title = parts[0]
            val category = parts[1]
            val amount = parseAmount(parts[2]) ?: return@mapNotNull null
            val month = if (parts.size >= 4) parts[3] else "settembre 26"
            Expense(title, category, amount, month)
        } else null
    }
}

private fun saveExpenses(context: Context, expenses: List<Expense>) {
    val raw = expenses.joinToString("\\n") { "${it.title}\\t${it.category}\\t${it.amount}\\t${it.month}" }
    context.getSharedPreferences(ExpenseStore, 0).edit().putString("items", raw).apply()
}""",
"""private fun loadExpenses(context: Context): List<Expense> {
    val prefs = context.getSharedPreferences(ExpenseStore, 0)
    if (!prefs.contains("items")) return emptyList()
    val raw = prefs.getString("items", "") ?: ""
    if (raw.isBlank()) return emptyList()
    return raw.lines().mapNotNull { line ->
        val parts = line.split("\\t")
        if (parts.size >= 3) {
            val title = parts[0]
            val category = parts[1]
            val amount = parseAmount(parts[2]) ?: return@mapNotNull null
            val month = if (parts.size >= 4) parts[3] else "settembre 26"
            val date = if (parts.size >= 5) parts[4] else ""
            val time = if (parts.size >= 6) parts[5] else ""
            val description = if (parts.size >= 7) parts[6] else ""
            Expense(title, category, amount, month, date, time, description)
        } else null
    }
}

private fun saveExpenses(context: Context, expenses: List<Expense>) {
    val raw = expenses.joinToString("\\n") { "${it.title}\\t${it.category}\\t${it.amount}\\t${it.month}\\t${it.date}\\t${it.time}\\t${it.description}" }
    context.getSharedPreferences(ExpenseStore, 0).edit().putString("items", raw).apply()
}""")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

