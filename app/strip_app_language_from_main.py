import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Remove lang_def from MainActivity.kt if present
lang_def = """enum class AppLanguage(val code: String, val displayName: String, val flag: String) {
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
}"""

content = content.replace(lang_def, "")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("AppLanguage stripped from MainActivity.kt")

