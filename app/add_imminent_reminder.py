import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update Dashboard parameters to include `reminders: List<PaymentReminder>`
dash_def_target = """private fun Dashboard(
    expenses: List<Expense>,
    total: Double,
    budget: Double?,
    numMonths: Int,
    availableMonths: List<String>,
    selectedMonth: String?,
    isDark: Boolean,
    isPrivacyMode: Boolean,"""

dash_def_repl = """private fun Dashboard(
    expenses: List<Expense>,
    total: Double,
    budget: Double?,
    numMonths: Int,
    availableMonths: List<String>,
    selectedMonth: String?,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    reminders: List<PaymentReminder>,"""

content = content.replace(dash_def_target, dash_def_repl)

# Update Dashboard call in SpeseApp
dash_call_target = """                        0 -> Dashboard(
                            expenses = activeMonthExpenses,
                            total = total,
                            budget = monthlyBudget,
                            numMonths = activeNumMonths,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,"""

dash_call_repl = """                        0 -> Dashboard(
                            expenses = activeMonthExpenses,
                            total = total,
                            budget = monthlyBudget,
                            numMonths = activeNumMonths,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,
                            reminders = reminders,"""

content = content.replace(dash_call_target, dash_call_repl)

# 2. Render imminent reminder card inside Dashboard (e.g. right after SummaryCard)
summary_card_target = """        item { SummaryCard(total, budget, expenses, numMonths, isDark, isPrivacyMode, onSetBudgetClick) }"""

imminent_card_code = """        item { SummaryCard(total, budget, expenses, numMonths, isDark, isPrivacyMode, onSetBudgetClick) }

        if (reminders.isNotEmpty()) {
            item {
                val nextReminder = reminders.firstOrNull()
                if (nextReminder != null) {
                    val cardBg = if (isDark) Color(0xFF2A2724) else Color.White
                    Surface(
                        color = cardBg,
                        shape = RoundedCornerShape(20.dp),
                        shadowElevation = 2.dp,
                        modifier = Modifier.fillMaxWidth()
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
                                text = "${String.format(Locale.getDefault(), "%.2f", nextReminder.amount)} €",
                                color = textColor,
                                fontWeight = FontWeight.ExtraBold,
                                fontSize = 15.sp
                            )
                        }
                    }
                }
            }
        }"""

content = content.replace(summary_card_target, imminent_card_code)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Imminent reminder added to Dashboard successfully.")

