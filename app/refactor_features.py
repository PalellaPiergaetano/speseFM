import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Fix ExpenseRow to accept onClick and be clickable
old_row_def = """@Composable
private fun ExpenseRow(expense: Expense, isDark: Boolean, isPrivacyMode: Boolean, onDelete: (Expense) -> Unit) {"""

new_row_def = """@Composable
private fun ExpenseRow(expense: Expense, isDark: Boolean, isPrivacyMode: Boolean, onClick: () -> Unit, onDelete: (Expense) -> Unit) {"""

content = content.replace(old_row_def, new_row_def)

old_row_surface = """    Surface(
        color = cardBg,
        shape = RoundedCornerShape(22.dp),
        shadowElevation = 1.dp,
        modifier = Modifier.fillMaxWidth()
    ) {"""

new_row_surface = """    Surface(
        color = cardBg,
        shape = RoundedCornerShape(22.dp),
        shadowElevation = 1.dp,
        modifier = Modifier.fillMaxWidth().clickable { onClick() }
    ) {"""

content = content.replace(old_row_surface, new_row_surface)

# Update ExpenseRow calls in Dashboard and Movements
content = content.replace("ExpenseRow(it, isDark, isPrivacyMode, onDeleteExpense)", "ExpenseRow(it, isDark, isPrivacyMode, onClick = { selectedExpense = it }, onDelete = onDeleteExpense)")

# 2. Move Reminders from bottom bar to SettingsScreen
# Remove 4th tab from BottomBar
old_bottom_bar = """                                listOf(
                                    AppStrings.get(AppStrings.panoramica_spese, appLang) to Icons.Default.Home,
                                    AppStrings.get(AppStrings.movimenti, appLang) to Icons.AutoMirrored.Filled.ReceiptLong,
                                    AppStrings.get(AppStrings.report_statistiche, appLang) to Icons.Default.BarChart,
                                    AppStrings.get(AppStrings.promemoria, appLang) to Icons.Default.Notifications
                                ).forEachIndexed { index, item ->"""

new_bottom_bar = """                                listOf(
                                    AppStrings.get(AppStrings.panoramica_spese, appLang) to Icons.Default.Home,
                                    AppStrings.get(AppStrings.movimenti, appLang) to Icons.AutoMirrored.Filled.ReceiptLong,
                                    AppStrings.get(AppStrings.report_statistiche, appLang) to Icons.Default.BarChart
                                ).forEachIndexed { index, item ->"""

content = content.replace(old_bottom_bar, new_bottom_bar)

# Remove case 3 from when(selectedTab) and handle reminders via Settings state (`showRemindersScreen`)
# Let's add `var showRemindersScreen by remember { mutableStateOf(false) }` in SpeseApp
content = content.replace("var selectedExpense by remember { mutableStateOf<Expense?>(null) }", "var selectedExpense by remember { mutableStateOf<Expense?>(null) }\n    var showRemindersScreen by remember { mutableStateOf(false) }")

# Remove `3 -> RemindersScreen(...)` from `when(selectedTab)`
reminders_when_block = """                        3 -> RemindersScreen(
                            reminders = reminders,
                            isDark = isDarkTheme,
                            onAddReminder = { 
                                reminders = reminders + it
                                savePaymentReminders(context, reminders)
                                Toast.makeText(context, AppStrings.get(AppStrings.promemoria_salvato, appLang), Toast.LENGTH_SHORT).show()
                            },
                            onDeleteReminder = { 
                                reminders = reminders.filter { r -> r != it }
                                savePaymentReminders(context, reminders)
                            },
                            onPayReminder = { reminder ->
                                val newExp = Expense(title = reminder.title, category = "Fitto / Bollette / Casa", amount = reminder.amount, month = currentMonth, date = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date()), time = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date()))
                                expenses = expenses + newExp
                                saveExpenses(context, expenses)
                                
                                reminders = reminders.map { r ->
                                    if (r == reminder) {
                                        r.copy(paymentsMade = r.paymentsMade + 1)
                                    } else r
                                }
                                savePaymentReminders(context, reminders)
                                Toast.makeText(context, "Pagamento registrato!", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.padding(padding)
                        )"""

content = content.replace(reminders_when_block, "")

# Add `showRemindersScreen` routing in SpeseApp (similar to showSettings)
routing_target = """                if (selectedExpense != null) {
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
                } else if (showSettings) {"""

routing_repl = """                if (selectedExpense != null) {
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
                            Toast.makeText(context, AppStrings.get(AppStrings.promemoria_salvato, appLang), Toast.LENGTH_SHORT).show()
                        },
                        onDeleteReminder = { 
                            reminders = reminders.filter { r -> r != it }
                            savePaymentReminders(context, reminders)
                        },
                        onPayReminder = { reminder ->
                            val newExp = Expense(title = reminder.title, category = "Fitto / Bollette / Casa", amount = reminder.amount, month = currentMonth, date = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date()), time = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date()))
                            expenses = expenses + newExp
                            saveExpenses(context, expenses)
                            
                            reminders = reminders.map { r ->
                                if (r == reminder) {
                                    r.copy(paymentsMade = r.paymentsMade + 1)
                                } else r
                            }
                            savePaymentReminders(context, reminders)
                            Toast.makeText(context, "Pagamento registrato!", Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier,
                        onClose = { showRemindersScreen = false }
                    )
                } else if (showSettings) {"""

content = content.replace(routing_target, routing_repl)

# Update RemindersScreen to support onClose for the TopAppBar back button when opened from settings
reminders_screen_target = """    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(AppStrings.get(AppStrings.promemoria_pagamenti, appLang), color = textColor, fontWeight = FontWeight.Bold, fontSize = 28.sp) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },"""

reminders_screen_repl = """    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(AppStrings.get(AppStrings.promemoria_pagamenti, appLang), color = textColor, fontWeight = FontWeight.Bold, fontSize = 28.sp) },
                navigationIcon = {
                    if (onClose != null) {
                        IconButton(onClick = onClose) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = AppStrings.get(AppStrings.indietro, appLang), tint = textColor)
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },"""

content = content.replace(reminders_screen_target, reminders_screen_repl)

# Update RemindersScreen signature to include `onClose: (() -> Unit)? = null`
content = content.replace(
    "fun RemindersScreen(\n    reminders: List<PaymentReminder>,\n    isDark: Boolean,\n    onAddReminder: (PaymentReminder) -> Unit,\n    onDeleteReminder: (PaymentReminder) -> Unit,\n    onPayReminder: (PaymentReminder) -> Unit,\n    modifier: Modifier\n)",
    "fun RemindersScreen(\n    reminders: List<PaymentReminder>,\n    isDark: Boolean,\n    onAddReminder: (PaymentReminder) -> Unit,\n    onDeleteReminder: (PaymentReminder) -> Unit,\n    onPayReminder: (PaymentReminder) -> Unit,\n    modifier: Modifier,\n    onClose: (() -> Unit)? = null\n)"
)

# Add Reminders item in SettingsScreen
settings_items_target = """            SettingsItemRow(
                icon = Icons.Default.Language,
                title = AppStrings.get(AppStrings.lingua, appLang),
                subtitle = appLang.displayName,
                onClick = onLanguageClick,
                isDark = isDark,
                cardBg = cardBg,
                textColor = textColor
            )"""

settings_items_repl = """            SettingsItemRow(
                icon = Icons.Default.Language,
                title = AppStrings.get(AppStrings.lingua, appLang),
                subtitle = appLang.displayName,
                onClick = onLanguageClick,
                isDark = isDark,
                cardBg = cardBg,
                textColor = textColor
            )

            SettingsItemRow(
                icon = Icons.Default.Notifications,
                title = AppStrings.get(AppStrings.promemoria_pagamenti, appLang),
                subtitle = AppStrings.get(AppStrings.scadenze, appLang),
                onClick = onRemindersClick,
                isDark = isDark,
                cardBg = cardBg,
                textColor = textColor
            )"""

content = content.replace(settings_items_target, settings_items_repl)

# Update SettingsScreen signature to accept `onRemindersClick: () -> Unit`
content = content.replace(
    "fun SettingsScreen(\n    isDark: Boolean,\n    isPrivacyMode: Boolean,\n    onTogglePrivacy: () -> Unit,\n    onLockClick: () -> Unit,\n    onImportClick: () -> Unit,\n    onExportClick: () -> Unit,\n    onClearAllClick: () -> Unit,\n    onOpenTutorialClick: () -> Unit,\n    onLanguageClick: () -> Unit,\n    onClose: () -> Unit\n)",
    "fun SettingsScreen(\n    isDark: Boolean,\n    isPrivacyMode: Boolean,\n    onTogglePrivacy: () -> Unit,\n    onLockClick: () -> Unit,\n    onImportClick: () -> Unit,\n    onExportClick: () -> Unit,\n    onClearAllClick: () -> Unit,\n    onOpenTutorialClick: () -> Unit,\n    onLanguageClick: () -> Unit,\n    onRemindersClick: () -> Unit,\n    onClose: () -> Unit\n)"
)

# Pass onRemindersClick from SpeseApp to SettingsScreen
content = content.replace(
    "onLanguageClick = onOpenLanguageDialog,",
    "onLanguageClick = onOpenLanguageDialog,\n                        onRemindersClick = { showRemindersScreen = true; showSettings = false },"
)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

