import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add dummy importXlsToExpenses and exportCsv
dummies = """
fun importXlsToExpenses(context: Context, uri: Uri, onResult: (List<Expense>) -> Unit) {
    Toast.makeText(context, "Importazione non supportata in questa versione", Toast.LENGTH_SHORT).show()
    onResult(emptyList())
}

fun exportCsv(context: Context, uri: Uri, expenses: List<Expense>) {
    Toast.makeText(context, "Esportazione non supportata in questa versione", Toast.LENGTH_SHORT).show()
}

"""
if "fun importXlsToExpenses" not in content:
    content = content + "\n" + dummies

# Fix mapColumnToCategory unresolved.
# `mapColumnToCategory` was a private function in the original file, wait, is it?
if "mapColumnToCategory" not in content:
    pass # Wait, it is in the file but maybe not accessible? Let's check if it exists.

# Fix missing arguments in Dashboard and Movements calls.
# `onOpenSettingsClick` and `onExpenseClick` were not passed in all usages.
# Where are they called? Inside `SpeseApp`!
# Let's find `Dashboard(` calls inside SpeseApp.
dash_call_wrong = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            modifier = Modifier.padding(innerPadding)
                        )"""
dash_call_fixed = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            onOpenSettingsClick = { showSettings = true },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(innerPadding)
                        )"""
content = content.replace(dash_call_wrong, dash_call_fixed)

mov_call_wrong = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            modifier = Modifier.padding(innerPadding)
                        )"""
mov_call_fixed = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(innerPadding)
                        )"""
content = content.replace(mov_call_wrong, mov_call_fixed)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)
