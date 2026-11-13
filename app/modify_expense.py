import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Expense and PaymentReminder
content = content.replace("data class Expense(\n    val title: String,\n    val category: String,\n    val amount: Double,\n    val date: String\n)", "data class Expense(\n    val title: String,\n    val category: String,\n    val amount: Double,\n    val date: String,\n    val time: String = \"\",\n    val description: String = \"\"\n)")

content = content.replace("data class PaymentReminder(\n    val title: String,\n    val amount: Double,\n    val dueDate: String,\n    val isRecurring: Boolean = false,\n    val recurrenceInterval: String? = null // e.g., \"Mensile\", \"Annuale\"\n)", "data class PaymentReminder(\n    val title: String,\n    val amount: Double,\n    val dueDate: String,\n    val isRecurring: Boolean = false,\n    val recurrenceInterval: String? = null,\n    val maxPayments: Int? = null,\n    val paymentsMade: Int = 0\n)")

# 2. Add AppLanguage and LocalAppLanguage
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

# 3. Replace Icons.Default.Menu with Icons.Default.Settings in the TopAppBar
content = content.replace("imageVector = Icons.Default.Menu", "imageVector = Icons.Default.Settings")
content = content.replace('contentDescription = "Menu"', 'contentDescription = "Settings"')

# Let's save it.
with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)
