import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix Expense class
expense_target = """data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = "settembre 26"
)"""
expense_repl = """data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = "settembre 26",
    val date: String = "",
    val time: String = "",
    val description: String = ""
)"""
content = content.replace(expense_target, expense_repl)

# Fix Dashboard call missing arguments
dash_call_target = """                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.padding(padding)
                        )"""
dash_call_repl = """                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            onOpenSettingsClick = { showSettings = true },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(padding)
                        )"""
content = content.replace(dash_call_target, dash_call_repl, 1)

# Fix Movements call missing arguments
mov_call_target = """                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.padding(padding)
                        )"""
mov_call_repl = """                            onDeleteExpense = { exp ->
                                expenses = expenses.filter { it != exp }
                                saveExpenses(context, expenses)
                                Toast.makeText(context, "Spesa eliminata", Toast.LENGTH_SHORT).show()
                            },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(padding)
                        )"""
content = content.replace(mov_call_target, mov_call_repl, 1)

# Fix mapColumnToCategory unresolved.
# I actually need to fix `importXlsToExpenses` and `exportCsv`. 
# Wait, I didn't add the dummy functions successfully?
# Let's add them before SpeseApp
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
    content = content.replace("@Composable\nprivate fun SpeseApp(", dummies + "\n@Composable\nprivate fun SpeseApp(")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

# Now fix AppStrings.kt (duplicate `descrizione`)
with open("src/main/java/it/fm/spese/AppStrings.kt", "r") as f:
    strings_content = f.read()

# I will remove the duplicate `descrizione` at the end
# The one at the end was added by me:
dup = """    val descrizione = mapOf(
        AppLanguage.ITALIAN to "Descrizione",
        AppLanguage.ENGLISH to "Description",
        AppLanguage.FRENCH to "Description",
        AppLanguage.SPANISH to "Descripción"
    )"""
strings_content = strings_content.replace(dup, "")

with open("src/main/java/it/fm/spese/AppStrings.kt", "w") as f:
    f.write(strings_content)

