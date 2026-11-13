import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix Movements definition
mov_wrong = """    onDeleteExpense: (Expense) -> Unit,
    onOpenSettingsClick: () -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)"""
mov_fixed = """    onDeleteExpense: (Expense) -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)"""
content = content.replace(mov_wrong, mov_fixed)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

with open("src/main/java/it/fm/spese/AppStrings.kt", "r") as f:
    strings_content = f.read()

descrizione_str = """
    val descrizione = mapOf(
        AppLanguage.ITALIAN to "Descrizione",
        AppLanguage.ENGLISH to "Description",
        AppLanguage.FRENCH to "Description",
        AppLanguage.SPANISH to "Descripción"
    )
"""
if "val descrizione =" not in strings_content:
    strings_content = strings_content.replace("fun get(", descrizione_str + "    fun get(")

with open("src/main/java/it/fm/spese/AppStrings.kt", "w") as f:
    f.write(strings_content)

