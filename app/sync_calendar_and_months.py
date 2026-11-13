import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Add getCurrentCalendarMonth and getExpenseMonthFromDate helper functions
helpers = """
fun getCurrentCalendarMonth(): String {
    return java.text.SimpleDateFormat("MMMM yy", java.util.Locale.ITALIAN).format(java.util.Date()).lowercase()
}

fun getExpenseMonthFromDate(dateStr: String): String {
    if (dateStr.isBlank()) return getCurrentCalendarMonth()
    val formats = listOf("dd/MM/yyyy", "dd/MM/yy", "yyyy-MM-dd", "d/M/yyyy", "d/M/yy")
    for (fmt in formats) {
        try {
            val date = java.text.SimpleDateFormat(fmt, java.util.Locale.getDefault()).parse(dateStr)
            if (date != null) {
                return java.text.SimpleDateFormat("MMMM yy", java.util.Locale.ITALIAN).format(date).lowercase()
            }
        } catch (e: Exception) {}
    }
    return getCurrentCalendarMonth()
}
"""

if "fun getCurrentCalendarMonth" not in content:
    content = content.replace("private const val ExpenseStore = \"expense_store\"", helpers + "\n\nprivate const val ExpenseStore = \"expense_store\"")

# 2. Update availableMonths in SpeseApp to include current calendar month automatically
old_avail_months = """    val availableMonths = remember(expenses) {
        val list = expenses.map { it.month }.distinct()
        if (list.isEmpty()) listOf("settembre 26") else list
    }"""

new_avail_months = """    val availableMonths = remember(expenses) {
        val nowMonth = getCurrentCalendarMonth()
        val list = (listOf(nowMonth) + expenses.map { it.month }).distinct()
        list
    }"""

content = content.replace(old_avail_months, new_avail_months)

# 3. Update AddExpenseDialog confirmButton to derive month from date
old_ai_add = """                        val currentDate = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())
                        val currentTime = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())
                        onAdd(Expense(parsedAi.title, parsedAi.category, amount, currentMonth, date = currentDate, time = currentTime))"""

new_ai_add = """                        val currentDate = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())
                        val currentTime = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())
                        val derivedMonth = getExpenseMonthFromDate(currentDate)
                        onAdd(Expense(parsedAi.title, parsedAi.category, amount, month = derivedMonth, date = currentDate, time = currentTime))"""

content = content.replace(old_ai_add, new_ai_add)

old_manual_add = """onAdd(Expense(manualTitle.ifBlank { "Spesa" }, manualCategory, parsedAmount, currentMonth, date = manualDate, time = manualTime))"""
new_manual_add = """val derivedMonth = getExpenseMonthFromDate(manualDate)
                            onAdd(Expense(manualTitle.ifBlank { "Spesa" }, manualCategory, parsedAmount, month = derivedMonth, date = manualDate, time = manualTime))"""

content = content.replace(old_manual_add, new_manual_add)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Calendar and month synchronization applied successfully.")

