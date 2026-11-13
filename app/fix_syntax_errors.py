import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix savePaymentReminders string concatenation
old_save = """private fun savePaymentReminders(context: Context, reminders: List<PaymentReminder>) {
    val raw = reminders.joinToString("\n") { "${it.title}\t${it.amount}\t${it.dueDate}\t${it.isRecurring}\t${it.recurrenceInterval}\t${it.maxPayments}\t${it.paymentsMade}" }
    context.getSharedPreferences(ReminderStore, 0).edit().putString("items", raw).apply()
}"""

new_save = """private fun savePaymentReminders(context: Context, reminders: List<PaymentReminder>) {
    val raw = reminders.joinToString("\\n") { it.title + "\t" + it.amount + "\t" + it.dueDate + "\t" + it.isRecurring + "\t" + it.recurrenceInterval + "\t" + it.maxPayments + "\t" + it.paymentsMade }
    context.getSharedPreferences(ReminderStore, 0).edit().putString("items", raw).apply()
}"""

content = content.replace(old_save, new_save)

# Remove duplicate `val appLang = LocalAppLanguage.current` declarations
# We can use a regex to replace `val appLang = LocalAppLanguage.current\s+val appLang = LocalAppLanguage.current` with `val appLang = LocalAppLanguage.current`
content = re.sub(r'val appLang = LocalAppLanguage\.current\s+val appLang = LocalAppLanguage\.current', r'val appLang = LocalAppLanguage.current', content)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

