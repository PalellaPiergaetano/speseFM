import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Expense data class update
content = content.replace(
    """data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = "settembre 26"
)""",
    """data class Expense(
    val title: String,
    val category: String,
    val amount: Double,
    val month: String = "settembre 26",
    val date: String = "",
    val time: String = "",
    val description: String = ""
)"""
)

# 2. PaymentReminder data class and persistence
reminder_model_code = """
data class PaymentReminder(
    val title: String,
    val amount: Double,
    val dueDate: String,
    val isRecurring: Boolean = false,
    val recurrenceInterval: String? = null,
    val maxPayments: Int? = null,
    val paymentsMade: Int = 0
)

private const val ReminderStore = "reminder_store"

private fun loadPaymentReminders(context: Context): List<PaymentReminder> {
    val prefs = context.getSharedPreferences(ReminderStore, 0)
    val raw = prefs.getString("items", "") ?: ""
    if (raw.isBlank()) return emptyList()
    return raw.lines().mapNotNull { line ->
        val parts = line.split("\\t")
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
    val raw = reminders.joinToString("\\n") { it.title + "\t" + it.amount + "\t" + it.dueDate + "\t" + it.isRecurring + "\t" + it.recurrenceInterval + "\t" + it.maxPayments + "\t" + it.paymentsMade }
    context.getSharedPreferences(ReminderStore, 0).edit().putString("items", raw).apply()
}
"""

content = content.replace("data class Expense(", reminder_model_code + "\n\ndata class Expense(")

# 3. AppLanguage & LocalAppLanguage
lang_def = """
enum class AppLanguage(val code: String, val displayName: String, val flag: String) {
    ITALIAN("it", "Italiano", "🇮🇹"),
    ENGLISH("en", "English", "🇬🇧"),
    FRENCH("fr", "Français", "🇫🇷"),
    SPANISH("es", "Español", "🇪🇸")
}

val LocalAppLanguage = androidx.compose.runtime.staticCompositionLocalOf { AppLanguage.ITALIAN }

fun loadAppLanguage(context: Context): AppLanguage {
    val prefs = context.getSharedPreferences("app_settings", Context.MODE_PRIVATE)
    val code = prefs.getString("language_code", "it") ?: "it"
    return AppLanguage.values().find { it.code == code } ?: AppLanguage.ITALIAN
}

fun saveAppLanguage(context: Context, language: AppLanguage) {
    val prefs = context.getSharedPreferences("app_settings", Context.MODE_PRIVATE)
    prefs.edit().putString("language_code", language.code).apply()
}
"""

content = content.replace("private val Violet = Color(0xFF6C5CE7)", "private val Violet = Color(0xFF6C5CE7)\n" + lang_def)

# 4. SpeseAppWithSecurity integration
sec_target = """    if (!isUnlocked) {
        SecurityLockOverlay(
            isDarkTheme = isDarkTheme,
            onUnlockClick = { triggerBiometric() }
        )
    } else {
        SpeseApp(
            onLockClick = { isUnlocked = false },
            launchImport = launchImport,
            launchExport = launchExport
        )
    }"""

sec_repl = """    var currentLanguage by remember { mutableStateOf(loadAppLanguage(activity)) }
    var showLanguageDialog by remember { mutableStateOf(false) }

    androidx.compose.runtime.CompositionLocalProvider(LocalAppLanguage provides currentLanguage) {
        if (showLanguageDialog) {
            LanguageSettingsDialog(
                currentLanguage = currentLanguage,
                onLanguageSelected = { 
                    currentLanguage = it
                    saveAppLanguage(activity, it)
                },
                onDismiss = { showLanguageDialog = false }
            )
        }
        if (!isUnlocked) {
            SecurityLockOverlay(
                isDarkTheme = isDarkTheme,
                onUnlockClick = { triggerBiometric() }
            )
        } else {
            SpeseApp(
                onOpenLanguageDialog = { showLanguageDialog = true },
                onLockClick = { isUnlocked = false },
                launchImport = launchImport,
                launchExport = launchExport
            )
        }
    }"""

content = content.replace(sec_target, sec_repl)

# Update SpeseApp signature
content = content.replace("private fun SpeseApp(\n    onLockClick: () -> Unit,", "private fun SpeseApp(\n    onOpenLanguageDialog: () -> Unit,\n    onLockClick: () -> Unit,")

# 5. Settings Icon in Dashboard & Reminders integration
# Replace QuickActionsStrip in Dashboard with nothing (or remove it)
content = re.sub(r'item\s*\{\s*QuickActionsStrip\(.*?\}\n\n\s*if \(!isPrivacyMode\)', r'if (!isPrivacyMode)', content, flags=re.DOTALL)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Clean refactor phase 1 applied.")

