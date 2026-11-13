import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Let's target AddExpenseDialog function
# We can inject `val appLang = LocalAppLanguage.current` at the beginning of AddExpenseDialog
old_dialog_start = """private fun AddExpenseDialog(
    currentMonth: String,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (Expense) -> Unit
) {
    var selectedTabMode by remember { mutableStateOf(0) } // 0 = IA, 1 = Manuale"""

new_dialog_start = """private fun AddExpenseDialog(
    currentMonth: String,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (Expense) -> Unit
) {
    val appLang = LocalAppLanguage.current
    var selectedTabMode by remember { mutableStateOf(0) } // 0 = IA, 1 = Manuale"""

content = content.replace(old_dialog_start, new_dialog_start)

# Now replace hardcoded texts in AddExpenseDialog
content = content.replace('Text("Nuova Spesa"', 'Text(AppStrings.get(AppStrings.nuova_spesa, appLang)')
content = content.replace('Text("Inserimento IA"', 'Text(AppStrings.get(AppStrings.inserimento_ia, appLang)')
content = content.replace('Text("Manuale"', 'Text(AppStrings.get(AppStrings.manuale, appLang)')
content = content.replace('Text("Suggerimenti rapidi:"', 'Text(AppStrings.get(AppStrings.suggerimenti_rapidi, appLang)')
content = content.replace('Text("Anteprima IA"', 'Text(AppStrings.get(AppStrings.anteprima_ia, appLang)')
content = content.replace('label = { Text("Descrizione") }', 'label = { Text(AppStrings.get(AppStrings.descrizione, appLang)) }')
content = content.replace('label = { Text("Importo (€)") }', 'label = { Text(AppStrings.get(AppStrings.importo, appLang)) }')
content = content.replace('Text("Categoria"', 'Text(AppStrings.get(AppStrings.categoria, appLang)')
content = content.replace('label = { Text("Seleziona categoria") }', 'label = { Text(AppStrings.get(AppStrings.seleziona_categoria, appLang)) }')
content = content.replace('Text("Annulla", color = Sage)', 'Text(AppStrings.get(AppStrings.annulla, appLang), color = Sage)')

# Add date and time to Expense creation inside AddExpenseDialog
old_add_1 = 'onAdd(Expense(parsedAi.title, parsedAi.category, amount, currentMonth))'
new_add_1 = """val currentDate = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())
                        val currentTime = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())
                        onAdd(Expense(parsedAi.title, parsedAi.category, amount, currentMonth, date = currentDate, time = currentTime))"""
content = content.replace(old_add_1, new_add_1)

old_add_2 = 'onAdd(Expense(manualTitle.ifBlank { "Spesa" }, manualCategory, parsedAmount, currentMonth))'
new_add_2 = """val currentDate = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())
                            val currentTime = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())
                            onAdd(Expense(manualTitle.ifBlank { "Spesa" }, manualCategory, parsedAmount, currentMonth, date = currentDate, time = currentTime))"""
content = content.replace(old_add_2, new_add_2)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

