import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update Expense data class
content = content.replace(
    """data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = "settembre 26"
)""",
    """data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = "settembre 26",
    val date: String = "",
    val time: String = "",
    val description: String = ""
)"""
)

# 2. Add PaymentReminder data class & persistence
reminder_model_code = """
data class PaymentReminder(
    val title: String,
    val amount: Double,
    val dueDate: String,
    val isRecurring: Boolean = false,
    val recurrenceInterval: String? = null,
    val maxPayments: Int? = null,
    val paymentsMade: Int = 0
)

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

fun importXlsToExpenses(context: Context, uri: Uri, onResult: (List<Expense>) -> Unit) {
    try {
        val imported = XlsSheetImporter.importFromUri(context, uri)
        if (imported.isNotEmpty()) {
            Toast.makeText(context, "Importati ${imported.size} movimenti con successo!", Toast.LENGTH_LONG).show()
            onResult(imported)
        } else {
            Toast.makeText(context, "Nessun movimento trovato nel file.", Toast.LENGTH_LONG).show()
            onResult(emptyList())
        }
    } catch (e: Exception) {
        Toast.makeText(context, "Errore durante l'importazione", Toast.LENGTH_SHORT).show()
        onResult(emptyList())
    }
}

fun exportCsv(context: Context, uri: Uri, expenses: List<Expense>) {
    val ok = exportExpensesToCsv(context, uri, expenses)
    if (ok) {
        Toast.makeText(context, "Backup CSV esportato con successo!", Toast.LENGTH_LONG).show()
    } else {
        Toast.makeText(context, "Errore durante l'esportazione CSV.", Toast.LENGTH_SHORT).show()
    }
}
"""

if "data class PaymentReminder" not in content:
    content = content.replace("data class Expense(", reminder_model_code + "\n\ndata class Expense(")

# 3. Update loadExpenses and saveExpenses to handle date, time, and description
old_load_save = """private fun loadExpenses(context: Context): List<Expense> {
    val prefs = context.getSharedPreferences(ExpenseStore, 0)
    if (!prefs.contains("items")) return emptyList()
    val raw = prefs.getString("items", "") ?: ""
    if (raw.isBlank()) return emptyList()
    return raw.lines().mapNotNull { line ->
        val parts = line.split("\t")
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
    val raw = expenses.joinToString("\n") { "${it.title}\t${it.category}\t${it.amount}\t${it.month}" }
    context.getSharedPreferences(ExpenseStore, 0).edit().putString("items", raw).apply()
}"""

new_load_save = """private fun loadExpenses(context: Context): List<Expense> {
    val prefs = context.getSharedPreferences(ExpenseStore, 0)
    if (!prefs.contains("items")) return emptyList()
    val raw = prefs.getString("items", "") ?: ""
    if (raw.isBlank()) return emptyList()
    return raw.lines().mapNotNull { line ->
        val parts = line.split("\t")
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
    val raw = expenses.joinToString("\n") { "${it.title}\t${it.category}\t${it.amount}\t${it.month}\t${it.date}\t${it.time}\t${it.description}" }
    context.getSharedPreferences(ExpenseStore, 0).edit().putString("items", raw).apply()
}"""

content = content.replace(old_load_save, new_load_save)

# 4. SpeseAppWithSecurity integration
sec_target = """    if (!isUnlocked) {
        SecurityLockOverlay(
            isDarkTheme = isDarkTheme,
            onUnlockClick = { triggerBiometric() }
        )
    } else {
        SpeseApp(
            onLockClick = { isUnlocked = false },
            launchImport = launchImport,
            launchExport = launchExport
        )
    }"""

sec_repl = """    var currentLanguage by remember { mutableStateOf(loadAppLanguage(activity)) }
    var showLanguageDialog by remember { mutableStateOf(false) }

    androidx.compose.runtime.CompositionLocalProvider(LocalAppLanguage provides currentLanguage) {
        if (showLanguageDialog) {
            LanguageSettingsDialog(
                currentLanguage = currentLanguage,
                onLanguageSelected = { 
                    currentLanguage = it
                    saveAppLanguage(activity, it)
                },
                onDismiss = { showLanguageDialog = false }
            )
        }
        if (!isUnlocked) {
            SecurityLockOverlay(
                isDarkTheme = isDarkTheme,
                onUnlockClick = { triggerBiometric() }
            )
        } else {
            SpeseApp(
                onOpenLanguageDialog = { showLanguageDialog = true },
                onLockClick = { isUnlocked = false },
                launchImport = launchImport,
                launchExport = launchExport
            )
        }
    }"""

content = content.replace(sec_target, sec_repl)

# Update SpeseApp signature
content = content.replace("private fun SpeseApp(\n    onLockClick: () -> Unit,", "private fun SpeseApp(\n    onOpenLanguageDialog: () -> Unit,\n    onLockClick: () -> Unit,")

# 5. SpeseApp state variables and routing
state_target = """    var showAddDialog by remember { mutableStateOf(false) }
    var showBudgetDialog by remember { mutableStateOf(false) }
    var showClearConfirmDialog by remember { mutableStateOf(false) }"""

state_repl = """    var showAddDialog by remember { mutableStateOf(false) }
    var showBudgetDialog by remember { mutableStateOf(false) }
    var showClearConfirmDialog by remember { mutableStateOf(false) }
    var reminders by remember { mutableStateOf(loadPaymentReminders(context)) }
    var showSettings by remember { mutableStateOf(false) }
    var selectedExpense by remember { mutableStateOf<Expense?>(null) }
    var showRemindersScreen by remember { mutableStateOf(false) }"""

content = content.replace(state_target, state_repl)

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

route_target = """            Box(modifier = Modifier.fillMaxSize().background(paperColor)) {
                BackgroundCircles(isDarkTheme)

                Scaffold("""

route_repl = """            Box(modifier = Modifier.fillMaxSize().background(paperColor)) {
                BackgroundCircles(isDarkTheme)

                if (selectedExpense != null) {
                    BackHandler { selectedExpense = null }
                    ExpenseDetailScreen(
                        expense = selectedExpense!!,
                        isDark = isDarkTheme,
                        onClose = { selectedExpense = null },
                        onDelete = { 
                            val e = selectedExpense!!
                            expenses = expenses.filter { it != e }
                            saveExpenses(context, expenses)
                            selectedExpense = null
                        },
                        onSaveEdit = { updated ->
                            expenses = expenses.map { if (it == selectedExpense) updated else it }
                            saveExpenses(context, expenses)
                            selectedExpense = updated
                        }
                    )
                } else if (showRemindersScreen) {
                    BackHandler { showRemindersScreen = false }
                    RemindersScreen(
                        reminders = reminders,
                        isDark = isDarkTheme,
                        onAddReminder = { 
                            reminders = reminders + it
                            savePaymentReminders(context, reminders)
                            Toast.makeText(context, AppStrings.get(AppStrings.promemoria_salvato, AppLanguage.ITALIAN), Toast.LENGTH_SHORT).show()
                        },
                        onDeleteReminder = { 
                            reminders = reminders.filter { r -> r != it }
                            savePaymentReminders(context, reminders)
                        },
                        onPayReminder = { reminder ->
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
                            Toast.makeText(context, AppStrings.get(AppStrings.promemoria_salvato, AppLanguage.ITALIAN), Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier,
                        onClose = { showRemindersScreen = false }
                    )
                } else if (showSettings) {
                    BackHandler { showSettings = false }
                    SettingsScreen(
                        isDark = isDarkTheme,
                        isPrivacyMode = isPrivacyMode,
                        onTogglePrivacy = { 
                            isPrivacyMode = !isPrivacyMode
                            savePrivacyMode(context, isPrivacyMode)
                        },
                        onLockClick = onLockClick,
                        onImportClick = { launchImport { uri -> uri?.let { importXlsToExpenses(context, it) { newExp -> expenses = expenses + newExp; saveExpenses(context, expenses) } } } },
                        onExportClick = { launchExport("Spese_FM_Backup_${System.currentTimeMillis()}.csv") { uri -> uri?.let { exportCsv(context, it, expenses) } } },
                        onClearAllClick = { showClearConfirmDialog = true },
                        onOpenTutorialClick = { showTutorial = true; showSettings = false },
                        onLanguageClick = onOpenLanguageDialog,
                        onRemindersClick = { showRemindersScreen = true; showSettings = false },
                        onClose = { showSettings = false }
                    )
                } else {
                    if (selectedTab != 0) {
                        BackHandler { selectedTab = 0 }
                    }
                Scaffold("""

content = content.replace(route_target, route_repl)

# Close `else` branch of Scaffold inside SpeseApp
close_target = """        )
    }
}

data class TutorialStep("""

close_repl = """        )
    }
}
}

data class TutorialStep("""

content = content.replace(close_target, close_repl)

# Remove QuickActionsStrip from Dashboard
content = re.sub(r'item\s*\{\s*QuickActionsStrip\(.*?\}\n\n\s*if \(!isPrivacyMode\)', r'if (!isPrivacyMode)', content, flags=re.DOTALL)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Full app rebuilder phase 1 complete.")

