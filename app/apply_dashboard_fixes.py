import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update Dashboard signature
old_dash_sig = """private fun Dashboard(
    expenses: List<Expense>,
    total: Double,
    budget: Double?,
    numMonths: Int,
    availableMonths: List<String>,
    selectedMonth: String?,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onTogglePrivacy: () -> Unit,
    onLockClick: () -> Unit,
    onOpenTutorialClick: () -> Unit,
    onMonthSelect: (String?) -> Unit,
    onCategoryClick: (String) -> Unit,
    onImportClick: () -> Unit,
    onExportClick: () -> Unit,
    onClearAllClick: () -> Unit,
    onSetBudgetClick: () -> Unit,
    onDeleteExpense: (Expense) -> Unit,
    modifier: Modifier
) {"""

new_dash_sig = """private fun Dashboard(
    expenses: List<Expense>,
    total: Double,
    budget: Double?,
    numMonths: Int,
    availableMonths: List<String>,
    selectedMonth: String?,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    reminders: List<PaymentReminder>,
    onTogglePrivacy: () -> Unit,
    onLockClick: () -> Unit,
    onOpenTutorialClick: () -> Unit,
    onMonthSelect: (String?) -> Unit,
    onCategoryClick: (String) -> Unit,
    onImportClick: () -> Unit,
    onExportClick: () -> Unit,
    onClearAllClick: () -> Unit,
    onSetBudgetClick: () -> Unit,
    onDeleteExpense: (Expense) -> Unit,
    onOpenSettingsClick: () -> Unit,
    onOpenRemindersClick: () -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
) {"""

content = content.replace(old_dash_sig, new_dash_sig)

# 2. Add Settings Icon in Dashboard header
old_title_row = """                Spacer(Modifier.height(2.dp))
                Text("Panoramica Spese", color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
            }"""

new_title_row = """                Spacer(Modifier.height(2.dp))
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                    Text(AppStrings.get(AppStrings.panoramica_spese, LocalAppLanguage.current), color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, modifier = Modifier.weight(1f))
                    androidx.compose.material3.IconButton(onClick = onOpenSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = textColor)
                    }
                }
            }"""

content = content.replace(old_title_row, new_title_row)

# 3. Remove QuickActionsStrip ("Gestione & Sicurezza") from Dashboard and add Imminent Reminder card
old_quick_actions_block = """        item {
            QuickActionsStrip(
                isPrivacyMode = isPrivacyMode,
                isDark = isDark,
                onTogglePrivacy = onTogglePrivacy,
                onLockClick = onLockClick,
                onOpenTutorialClick = onOpenTutorialClick,
                onImportClick = onImportClick,
                onExportClick = onExportClick,
                onClearAllClick = onClearAllClick
            )
        }"""

imminent_card_block = """        if (reminders.isNotEmpty()) {
            item {
                val nextReminder = reminders.firstOrNull()
                if (nextReminder != null) {
                    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
                    Surface(
                        color = cardBg,
                        shape = RoundedCornerShape(20.dp),
                        shadowElevation = 2.dp,
                        modifier = Modifier.fillMaxWidth().clickable { onOpenRemindersClick() }
                    ) {
                        Row(
                            modifier = Modifier.padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .background(Terracotta.copy(alpha = 0.15f), CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.NotificationsActive, contentDescription = null, tint = Terracotta, modifier = Modifier.size(20.dp))
                            }
                            Spacer(Modifier.width(14.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Prossima Scadenza", color = Terracotta, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                                Text(nextReminder.title, color = textColor, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                                Text("Scadenza: ${nextReminder.dueDate}", color = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68), fontSize = 12.sp)
                            }
                            Text(
                                text = "${String.format(java.util.Locale.getDefault(), "%.2f", nextReminder.amount)} €",
                                color = textColor,
                                fontWeight = FontWeight.ExtraBold,
                                fontSize = 15.sp
                            )
                        }
                    }
                }
            }
        }"""

content = content.replace(old_quick_actions_block, imminent_card_block)

# 4. Update Movements signature
old_mov_sig = """private fun Movements(
    expenses: List<Expense>,
    availableMonths: List<String>,
    selectedMonth: String?,
    initialCategoryFilter: String?,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onMonthSelect: (String?) -> Unit,
    onClearCategoryFilter: () -> Unit,
    onDeleteExpense: (Expense) -> Unit,
    modifier: Modifier
) {"""

new_mov_sig = """private fun Movements(
    expenses: List<Expense>,
    availableMonths: List<String>,
    selectedMonth: String?,
    initialCategoryFilter: String?,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onMonthSelect: (String?) -> Unit,
    onClearCategoryFilter: () -> Unit,
    onDeleteExpense: (Expense) -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
) {"""

content = content.replace(old_mov_sig, new_mov_sig)

# 5. Update ExpenseRow definition to accept onClick and make Surface clickable
old_exp_row_sig = """@Composable
private fun ExpenseRow(expense: Expense, isDark: Boolean, isPrivacyMode: Boolean, onDelete: (Expense) -> Unit) {"""

new_exp_row_sig = """@Composable
private fun ExpenseRow(expense: Expense, isDark: Boolean, isPrivacyMode: Boolean, onClick: () -> Unit, onDelete: (Expense) -> Unit) {"""

content = content.replace(old_exp_row_sig, new_exp_row_sig)

old_exp_row_surf = """    Surface(
        color = cardBg,
        shape = RoundedCornerShape(22.dp),
        shadowElevation = 1.dp,
        modifier = Modifier.fillMaxWidth()
    ) {"""

new_exp_row_surf = """    Surface(
        color = cardBg,
        shape = RoundedCornerShape(22.dp),
        shadowElevation = 1.dp,
        modifier = Modifier.fillMaxWidth().clickable { onClick() }
    ) {"""

content = content.replace(old_exp_row_surf, new_exp_row_surf)

# 6. Update ExpenseRow calls in Dashboard and Movements
content = content.replace("items(expenses.take(5)) { ExpenseRow(it, isDark, isPrivacyMode, onDeleteExpense) }", "items(expenses.take(5)) { ExpenseRow(it, isDark, isPrivacyMode, onClick = { onExpenseClick(it) }, onDelete = onDeleteExpense) }")
content = content.replace("items(filteredExpenses) { ExpenseRow(it, isDark, isPrivacyMode, onDeleteExpense) }", "items(filteredExpenses) { ExpenseRow(it, isDark, isPrivacyMode, onClick = { onExpenseClick(it) }, onDelete = onDeleteExpense) }")

# 7. Update Dashboard call inside SpeseApp
old_dash_call = """                        0 -> Dashboard(
                            expenses = activeMonthExpenses,
                            total = total,
                            budget = monthlyBudget,
                            numMonths = activeNumMonths,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,
                            onTogglePrivacy = {
                                isPrivacyMode = !isPrivacyMode
                                savePrivacyMode(context, isPrivacyMode)
                            },
                            onLockClick = onLockClick,
                            onOpenTutorialClick = { showTutorial = true },
                            onMonthSelect = { selectedMonthFilter = it },
                            onCategoryClick = { cat ->
                                selectedCategoryFilter = cat
                                selectedTab = 1
                            },
                            onImportClick = { launchImport { uri -> uri?.let { importXlsToExpenses(context, it) { newExp -> expenses = expenses + newExp; saveExpenses(context, expenses) } } } },
                            onExportClick = { launchExport("Spese_FM_Backup_${System.currentTimeMillis()}.csv") { uri -> uri?.let { exportCsv(context, it, expenses) } } },
                            onClearAllClick = { showClearConfirmDialog = true },
                            onSetBudgetClick = { showBudgetDialog = true },
                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.padding(padding)
                        )"""

new_dash_call = """                        0 -> Dashboard(
                            expenses = activeMonthExpenses,
                            total = total,
                            budget = monthlyBudget,
                            numMonths = activeNumMonths,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,
                            reminders = reminders,
                            onTogglePrivacy = {
                                isPrivacyMode = !isPrivacyMode
                                savePrivacyMode(context, isPrivacyMode)
                            },
                            onLockClick = onLockClick,
                            onOpenTutorialClick = { showTutorial = true },
                            onMonthSelect = { selectedMonthFilter = it },
                            onCategoryClick = { cat ->
                                selectedCategoryFilter = cat
                                selectedTab = 1
                            },
                            onImportClick = { launchImport { uri -> uri?.let { importXlsToExpenses(context, it) { newExp -> expenses = expenses + newExp; saveExpenses(context, expenses) } } } },
                            onExportClick = { launchExport("Spese_FM_Backup_${System.currentTimeMillis()}.csv") { uri -> uri?.let { exportCsv(context, it, expenses) } },
                            onClearAllClick = { showClearConfirmDialog = true },
                            onSetBudgetClick = { showBudgetDialog = true },
                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            onOpenSettingsClick = { showSettings = true },
                            onOpenRemindersClick = { showRemindersScreen = true },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(padding)
                        )"""

content = content.replace(old_dash_call, new_dash_call)

# 8. Update Movements call inside SpeseApp
old_mov_call = """                        1 -> Movements(
                            expenses = activeMonthExpenses,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            initialCategoryFilter = selectedCategoryFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,
                            onMonthSelect = { selectedMonthFilter = it },
                            onClearCategoryFilter = { selectedCategoryFilter = null },
                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.padding(padding)
                        )"""

new_mov_call = """                        1 -> Movements(
                            expenses = activeMonthExpenses,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            initialCategoryFilter = selectedCategoryFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,
                            onMonthSelect = { selectedMonthFilter = it },
                            onClearCategoryFilter = { selectedCategoryFilter = null },
                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(padding)
                        )"""

content = content.replace(old_mov_call, new_mov_call)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Dashboard fixes applied successfully.")

