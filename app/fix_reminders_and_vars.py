import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Replace Gson-based reminder storage with simple tab-separated storage
old_reminders_storage = """private fun loadPaymentReminders(context: Context): List<PaymentReminder> {
    val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
    val json = prefs.getString("payment_reminders", null) ?: return emptyList()
    val type = object : com.google.gson.reflect.TypeToken<List<PaymentReminder>>() {}.type
    return try {
        com.google.gson.Gson().fromJson(json, type) ?: emptyList()
    } catch (e: Exception) {
        emptyList()
    }
}

private fun savePaymentReminders(context: Context, reminders: List<PaymentReminder>) {
    val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
    val json = com.google.gson.Gson().toJson(reminders)
    prefs.edit().putString("payment_reminders", json).apply()
}"""

new_reminders_storage = """private const val ReminderStore = "reminder_store"

private fun loadPaymentReminders(context: Context): List<PaymentReminder> {
    val prefs = context.getSharedPreferences(ReminderStore, 0)
    val raw = prefs.getString("items", "") ?: ""
    if (raw.isBlank()) return emptyList()
    return raw.lines().mapNotNull { line ->
        val parts = line.split("\t")
        if (parts.size >= 3) {
            val title = parts[0]
            val amount = parseAmount(parts[1]) ?: return@mapNotNull null
            val dueDate = parts[2]
            val isRecurring = if (parts.size >= 4) parts[3].toBoolean() else false
            val interval = if (parts.size >= 5 && parts[4] != "null") parts[4] else null
            val maxP = if (parts.size >= 6) parts[5].toIntOrNull() else null
            val made = if (parts.size >= 7) parts[6].toIntOrNull() ?: 0 else 0
            PaymentReminder(title, amount, dueDate, isRecurring, interval, maxP, made)
        } else null
    }
}

private fun savePaymentReminders(context: Context, reminders: List<PaymentReminder>) {
    val raw = reminders.joinToString("\n") { "${it.title}\t${it.amount}\t${it.dueDate}\t${it.isRecurring}\t${it.recurrenceInterval}\t${it.maxPayments}\t${it.paymentsMade}" }
    context.getSharedPreferences(ReminderStore, 0).edit().putString("items", raw).apply()
}"""

content = content.replace(old_reminders_storage, new_reminders_storage)

# 2. Fix manualDate and manualTime scope in AddExpenseDialog
old_add_dialog_manual = """                // INSERIMENTO MANUALE
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    var manualDate by remember { mutableStateOf(java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())) }
                    var manualTime by remember { mutableStateOf(java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())) }"""

# Move manualDate and manualTime to top of AddExpenseDialog so confirmButton can access them
old_dialog_head = """private fun AddExpenseDialog(
    currentMonth: String,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (Expense) -> Unit
) {
    val appLang = LocalAppLanguage.current
    var selectedTabMode by remember { mutableStateOf(0) } // 0 = IA, 1 = Manuale"""

new_dialog_head = """private fun AddExpenseDialog(
    currentMonth: String,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (Expense) -> Unit
) {
    val appLang = LocalAppLanguage.current
    var selectedTabMode by remember { mutableStateOf(0) } // 0 = IA, 1 = Manuale
    var manualDate by remember { mutableStateOf(java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())) }
    var manualTime by remember { mutableStateOf(java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())) }"""

content = content.replace(old_dialog_head, new_dialog_head)

# Remove local declarations of manualDate and manualTime inside the Column
old_manual_col = """                // INSERIMENTO MANUALE
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    var manualDate by remember { mutableStateOf(java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())) }
                    var manualTime by remember { mutableStateOf(java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())) }"""

new_manual_col = """                // INSERIMENTO MANUALE
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {"""

content = content.replace(old_manual_col, new_manual_col)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

