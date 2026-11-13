import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

target = """    onDeleteExpense: (Expense) -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)

    LazyColumn("""

repl = """    onDeleteExpense: (Expense) -> Unit,
    onOpenSettingsClick: () -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)

    LazyColumn("""

content = content.replace(target, repl)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

