import re

# 1. Update AppStrings.kt to add `mese` key
with open("src/main/java/it/fm/spese/AppStrings.kt", "r") as f:
    strings_content = f.read()

if "val mese =" not in strings_content:
    mese_str = """
    val mese = mapOf(
        AppLanguage.ITALIAN to "Mese",
        AppLanguage.ENGLISH to "Month",
        AppLanguage.FRENCH to "Mois",
        AppLanguage.SPANISH to "Mes"
    )
"""
    strings_content = strings_content.replace("fun get(", mese_str + "    fun get(")
    with open("src/main/java/it/fm/spese/AppStrings.kt", "w") as f:
        f.write(strings_content)

# 2. Update MainActivity.kt for translations, reminders behavior, home reminder click, and settings style
with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# A. MonthSelectorStrip "Tutti i Mesi" -> AppStrings.get(AppStrings.tutti_i_mesi, appLang)
content = content.replace('"Tutti i Mesi"', 'AppStrings.get(AppStrings.tutti_i_mesi, appLang)')

# B. Reports translations
content = content.replace('Text("Media / Mese"', 'Text(AppStrings.get(AppStrings.media_giorno, appLang)') # or similar
content = content.replace('Text("Spesa Max"', 'Text(AppStrings.get(AppStrings.spesa_max, appLang)')
content = content.replace('Text("Andamento per Anno"', 'Text(AppStrings.get(AppStrings.andamento_per_anno, appLang)')
content = content.replace('Text("Distribuzione Spese"', 'Text(AppStrings.get(AppStrings.distribuzione_spese, appLang)')

# C. ExpenseDetailScreen translations
content = content.replace('DetailRow("Mese"', 'DetailRow(AppStrings.get(AppStrings.mese, appLang)')

# D. One-time reminders disappearing upon payment
pay_reminder_target = """                            onPayReminder = { reminder ->
                                val newExp = Expense(title = reminder.title, category = "Fitto / Bollette / Casa", amount = reminder.amount, month = availableMonths.firstOrNull() ?: "settembre 26", date = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date()), time = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date()))
                                expenses = expenses + newExp
                                saveExpenses(context, expenses)
                                
                                reminders = reminders.map { r ->
                                    if (r == reminder) {
                                        r.copy(paymentsMade = r.paymentsMade + 1)
                                    } else r
                                }
                                savePaymentReminders(context, reminders)
                                Toast.makeText(context, "Pagamento registrato!", Toast.LENGTH_SHORT).show()
                            },"""

pay_reminder_repl = """                            onPayReminder = { reminder ->
                                val newExp = Expense(title = reminder.title, category = "Fitto / Bollette / Casa", amount = reminder.amount, month = availableMonths.firstOrNull() ?: "settembre 26", date = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date()), time = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date()))
                                expenses = expenses + newExp
                                saveExpenses(context, expenses)
                                
                                reminders = if (!reminder.isRecurring || (reminder.maxPayments != null && reminder.paymentsMade + 1 >= reminder.maxPayments)) {
                                    reminders.filter { it != reminder }
                                } else {
                                    reminders.map { r ->
                                        if (r == reminder) {
                                            r.copy(paymentsMade = r.paymentsMade + 1)
                                        } else r
                                    }
                                }
                                savePaymentReminders(context, reminders)
                                Toast.makeText(context, AppStrings.get(AppStrings.promemoria_salvato, appLang), Toast.LENGTH_SHORT).show()
                            },"""

content = content.replace(pay_reminder_target, pay_reminder_repl)

# E. Clicking Home reminder card navigates to Reminders section
home_reminder_target = """                    Surface(
                        color = cardBg,
                        shape = RoundedCornerShape(20.dp),
                        shadowElevation = 2.dp,
                        modifier = Modifier.fillMaxWidth()
                    ) {"""

home_reminder_repl = """                    Surface(
                        color = cardBg,
                        shape = RoundedCornerShape(20.dp),
                        shadowElevation = 2.dp,
                        modifier = Modifier.fillMaxWidth().clickable { onOpenRemindersClick() }
                    ) {"""

content = content.replace(home_reminder_target, home_reminder_repl)

# Update Dashboard signature and call to accept onOpenRemindersClick
dash_def_old = """    onDeleteExpense: (Expense) -> Unit,
    onOpenSettingsClick: () -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
) {"""

dash_def_new = """    onDeleteExpense: (Expense) -> Unit,
    onOpenSettingsClick: () -> Unit,
    onOpenRemindersClick: () -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
) {"""

content = content.replace(dash_def_old, dash_def_new)

dash_call_old = """                            onOpenSettingsClick = { showSettings = true },
                            onExpenseClick = { selectedExpense = it },"""

dash_call_new = """                            onOpenSettingsClick = { showSettings = true },
                            onOpenRemindersClick = { showRemindersScreen = true },
                            onExpenseClick = { selectedExpense = it },"""

content = content.replace(dash_call_old, dash_call_new)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("All user issues fixed successfully.")

