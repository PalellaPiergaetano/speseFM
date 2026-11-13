import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add PaymentReminder and its persistence functions
reminder_storage_code = """
private const val ReminderStore = "reminder_store"

private fun loadPaymentReminders(context: Context): List<PaymentReminder> {
    val prefs = context.getSharedPreferences(ReminderStore, 0)
    val raw = prefs.getString("items", "") ?: ""
    if (raw.isBlank()) return emptyList()
    return raw.lines().mapNotNull { line ->
        val parts = line.split("\\t")
        if (parts.size >= 3) {
            val title = parts[0]
            val amount = parseAmount(parts[1]) ?: return@mapNotNull null
            val dueDate = parts[2]
            val isRecurring = if (parts.size >= 4) parts[3].toBoolean() else false
            val interval = if (parts.size >= 5 && parts[4] != "null") parts[4] else null
            val maxP = if (parts.size >= 6) parts[5].toIntOrNull() else null
            val made = if (parts.size >= 7) parts[6].toIntOrNull() ?: 0 else 0
            PaymentReminder(title, amount, dueDate, isRecurring, interval, maxP, made)
        } else null
    }
}

private fun savePaymentReminders(context: Context, reminders: List<PaymentReminder>) {
    val raw = reminders.joinToString("\\n") { it.title + "\t" + it.amount + "\t" + it.dueDate + "\t" + it.isRecurring + "\t" + it.recurrenceInterval + "\t" + it.maxPayments + "\t" + it.paymentsMade }
    context.getSharedPreferences(ReminderStore, 0).edit().putString("items", raw).apply()
}
"""

if "fun loadPaymentReminders" not in content:
    content = content.replace("private const val ExpenseStore = \"expense_store\"", reminder_storage_code + "\n\nprivate const val ExpenseStore = \"expense_store\"")

# Fix LocalAppLanguage.current inside Toast callbacks in RemindersScreen routing
content = content.replace(
    "Toast.makeText(context, AppStrings.get(AppStrings.promemoria_salvato, LocalAppLanguage.current), Toast.LENGTH_SHORT).show()",
    "Toast.makeText(context, AppStrings.get(AppStrings.promemoria_salvato, AppLanguage.ITALIAN), Toast.LENGTH_SHORT).show()"
)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Reminders storage and Toast callbacks fixed.")

