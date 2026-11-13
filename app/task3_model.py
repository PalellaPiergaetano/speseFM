import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Update Expense
content = content.replace(
"""data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = getCurrentMonthString(),
    val date: String = getCurrentDateString()
)""",
"""data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = getCurrentMonthString(),
    val date: String = getCurrentDateString(),
    val time: String = "",
    val description: String = ""
)""")

# Update loadExpenses
content = content.replace(
"""            val month = if (parts.size >= 4 && parts[3].isNotBlank()) parts[3] else getCurrentMonthString()
            val date = if (parts.size >= 5 && parts[4].isNotBlank()) parts[4] else getCurrentDateString()
            Expense(title, category, amount, month, date)
        } else null""",
"""            val month = if (parts.size >= 4 && parts[3].isNotBlank()) parts[3] else getCurrentMonthString()
            val date = if (parts.size >= 5 && parts[4].isNotBlank()) parts[4] else getCurrentDateString()
            val time = if (parts.size >= 6) parts[5] else ""
            val description = if (parts.size >= 7) parts[6] else ""
            Expense(title, category, amount, month, date, time, description)
        } else null""")

# Update saveExpenses
content = content.replace(
"""    val raw = expenses.joinToString("\\n") { "${it.title}\\t${it.category}\\t${it.amount}\\t${it.month}\\t${it.date}" }""",
"""    val raw = expenses.joinToString("\\n") { "${it.title}\\t${it.category}\\t${it.amount}\\t${it.month}\\t${it.date}\\t${it.time}\\t${it.description}" }""")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

