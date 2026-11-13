import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix conflicting declarations of showClearConfirmDialog
content = re.sub(r'var showClearConfirmDialog by remember \{ mutableStateOf\(false\) \}\n\s*var showClearConfirmDialog by remember \{ mutableStateOf\(false\) \}', r'var showClearConfirmDialog by remember { mutableStateOf(false) }', content)

# Fix LanguageSettingsDialog
content = content.replace("LanguageSettingsDialog(", "LanguageSettingsDialog(currentLanguage = AppLanguage.ITALIAN, onLanguageSelected = {}, onDismiss = {}) // TODO")

# Add loadAppLanguage and saveAppLanguage if missing
if "fun loadAppLanguage(" not in content:
    helpers = """
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
    content = content.replace("enum class AppLanguage", helpers + "enum class AppLanguage")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

