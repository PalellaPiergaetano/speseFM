import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Fix currentMonth inside onPayReminder
content = content.replace(
    "month = currentMonth",
    "month = availableMonths.firstOrNull() ?: \"settembre 26\""
)

# 2. Fix Dashboard and Movements calls to pass onExpenseClick properly
# In Dashboard call:
content = content.replace("onExpenseClick = { selectedExpense = it }", "onExpenseClick = { selectedExpense = it }")

# Wait, let's check Dashboard signature and call
# Dashboard call in SpeseApp:
dash_call = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            onOpenSettingsClick = { showSettings = true },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(innerPadding)"""

# Inside Dashboard, `ExpenseRow` should call `onExpenseClick(e)` instead of `selectedExpense = it`.
content = content.replace("onClick = { selectedExpense = it }", "onClick = { onExpenseClick(e) }")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

