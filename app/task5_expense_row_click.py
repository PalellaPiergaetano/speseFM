import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Update ExpenseRow definition
expense_row_def_target = """fun ExpenseRow(
    expense: Expense,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onDelete: () -> Unit
)"""
expense_row_def_repl = """fun ExpenseRow(
    expense: Expense,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onClick: () -> Unit,
    onDelete: () -> Unit
)"""
if expense_row_def_target in content:
    content = content.replace(expense_row_def_target, expense_row_def_repl)

# Add clickable modifier to ExpenseRow's Surface
expense_row_surface_target = """        shape = RoundedCornerShape(16.dp),
        shadowElevation = 2.dp,
        modifier = Modifier.fillMaxWidth()
    ) {"""
expense_row_surface_repl = """        shape = RoundedCornerShape(16.dp),
        shadowElevation = 2.dp,
        modifier = Modifier.fillMaxWidth().clickable { onClick() }
    ) {"""
if expense_row_surface_target in content:
    content = content.replace(expense_row_surface_target, expense_row_surface_repl)

# Add onExpenseClick to Dashboard
dash_def_target = """    onDeleteExpense: (Expense) -> Unit,
    onOpenSettingsClick: () -> Unit,
    modifier: Modifier
)"""
dash_def_repl = """    onDeleteExpense: (Expense) -> Unit,
    onOpenSettingsClick: () -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
)"""
if dash_def_target in content:
    content = content.replace(dash_def_target, dash_def_repl)

# Update Dashboard call in SpeseApp
dash_call_target = """                            onOpenSettingsClick = { showSettings = true },
                            modifier = Modifier.padding(innerPadding)
                        )"""
dash_call_repl = """                            onOpenSettingsClick = { showSettings = true },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(innerPadding)
                        )"""
if dash_call_target in content:
    content = content.replace(dash_call_target, dash_call_repl)

# Update ExpenseRow call in Dashboard
dash_expense_row_call_target = """ExpenseRow(
                        expense = e,
                        isDark = isDark,
                        isPrivacyMode = isPrivacyMode,
                        onDelete = { onDeleteExpense(e) }
                    )"""
dash_expense_row_call_repl = """ExpenseRow(
                        expense = e,
                        isDark = isDark,
                        isPrivacyMode = isPrivacyMode,
                        onClick = { onExpenseClick(e) },
                        onDelete = { onDeleteExpense(e) }
                    )"""
if dash_expense_row_call_target in content:
    content = content.replace(dash_expense_row_call_target, dash_expense_row_call_repl)

# Same for Movements page
mov_def_target = """    onDeleteExpense: (Expense) -> Unit,
    modifier: Modifier
)"""
mov_def_repl = """    onDeleteExpense: (Expense) -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
)"""
if mov_def_target in content:
    content = content.replace(mov_def_target, mov_def_repl)

mov_call_target = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            modifier = Modifier.padding(innerPadding)
                        )"""
mov_call_repl = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(innerPadding)
                        )"""
if mov_call_target in content:
    content = content.replace(mov_call_target, mov_call_repl)

mov_expense_row_call_target = """ExpenseRow(
                        expense = e,
                        isDark = isDark,
                        isPrivacyMode = isPrivacyMode,
                        onDelete = { onDeleteExpense(e) }
                    )"""
mov_expense_row_call_repl = """ExpenseRow(
                        expense = e,
                        isDark = isDark,
                        isPrivacyMode = isPrivacyMode,
                        onClick = { onExpenseClick(e) },
                        onDelete = { onDeleteExpense(e) }
                    )"""
if mov_expense_row_call_target in content:
    content = content.replace(mov_expense_row_call_target, mov_expense_row_call_repl)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

