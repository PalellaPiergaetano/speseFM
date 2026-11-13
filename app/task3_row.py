import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add clickable to ExpenseRow and the Dialog
content = content.replace(
"""private fun ExpenseRow(
    expense: Expense,
    isDarkTheme: Boolean,
    isPrivacyMode: Boolean,
    onDelete: (Expense) -> Unit
) {""",
"""private fun ExpenseRow(
    expense: Expense,
    isDarkTheme: Boolean,
    isPrivacyMode: Boolean,
    onDelete: (Expense) -> Unit
) {
    var showDetail by remember { mutableStateOf(false) }
    if (showDetail) {
        ExpenseDetailDialog(
            expense = expense,
            isDarkTheme = isDarkTheme,
            onDismiss = { showDetail = false }
        )
    }
""")

content = content.replace(
"""    Surface(
        color = cardBg,
        shape = RoundedCornerShape(24.dp),
        shadowElevation = 2.dp,
        modifier = Modifier.fillMaxWidth()
    ) {""",
"""    Surface(
        color = cardBg,
        shape = RoundedCornerShape(24.dp),
        shadowElevation = 2.dp,
        modifier = Modifier.fillMaxWidth().clickable { showDetail = true }
    ) {""")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

