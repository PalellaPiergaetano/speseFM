import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Declare manualDate and manualTime at top of AddExpenseDialog
old_head = """private fun AddExpenseDialog(
    currentMonth: String,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (Expense) -> Unit
) {
    var selectedTabMode by remember { mutableStateOf(0) } // 0 = IA, 1 = Manuale"""

new_head = """private fun AddExpenseDialog(
    currentMonth: String,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (Expense) -> Unit
) {
    var selectedTabMode by remember { mutableStateOf(0) } // 0 = IA, 1 = Manuale
    var manualDate by remember { mutableStateOf(java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())) }
    var manualTime by remember { mutableStateOf(java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())) }"""

content = content.replace(old_head, new_head)

# Remove local var manualDate/manualTime declarations inside Column
old_col = """                // INSERIMENTO MANUALE
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    val appLang = LocalAppLanguage.current
                    var manualDate by remember { mutableStateOf(java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())) }
                    var manualTime by remember { mutableStateOf(java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())) }"""

new_col = """                // INSERIMENTO MANUALE
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    val appLang = LocalAppLanguage.current"""

content = content.replace(old_col, new_col)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Dialog scope fixed.")

