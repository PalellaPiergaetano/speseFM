import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

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
                            onExportClick = { launchExport("Spese_FM_Backup_${System.currentTimeMillis()}.csv") { uri -> uri?.let { exportCsv(context, it, expenses) } } },
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

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("SpeseApp Dashboard call fixed.")

