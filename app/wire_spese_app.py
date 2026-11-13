import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Insert states in SpeseApp
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

# 2. Insert routing around Scaffold
route_target = """            Box(modifier = Modifier.fillMaxSize().background(paperColor)) {
                BackgroundCircles(isDarkTheme)

                Scaffold("""

route_repl = """            Box(modifier = Modifier.fillMaxSize().background(paperColor)) {
                BackgroundCircles(isDarkTheme)

                if (selectedExpense != null) {
                    ExpenseDetailScreen(
                        expense = selectedExpense!!,
                        isDark = isDarkTheme,
                        onClose = { selectedExpense = null },
                        onDelete = { 
                            val e = selectedExpense!!
                            expenses = expenses.filter { it != e }
                            saveExpenses(context, expenses)
                            selectedExpense = null
                        }
                    )
                } else if (showRemindersScreen) {
                    RemindersScreen(
                        reminders = reminders,
                        isDark = isDarkTheme,
                        onAddReminder = { 
                            reminders = reminders + it
                            savePaymentReminders(context, reminders)
                            Toast.makeText(context, AppStrings.get(AppStrings.promemoria_salvato, LocalAppLanguage.current), Toast.LENGTH_SHORT).show()
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
                            Toast.makeText(context, AppStrings.get(AppStrings.promemoria_salvato, LocalAppLanguage.current), Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier,
                        onClose = { showRemindersScreen = false }
                    )
                } else if (showSettings) {
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
                Scaffold("""

content = content.replace(route_target, route_repl)

# 3. Close the `else` branch of Scaffold inside SpeseApp
# SpeseApp ends before `data class TutorialStep`
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

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("SpeseApp routing wired successfully.")

