import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Remove duplicate AppLanguage definition from MainActivity.kt
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

# Add all necessary imports
imports = """
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.NotificationsNone
import androidx.compose.material.icons.filled.NotificationsActive
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.Switch
import androidx.compose.material3.RadioButton
import androidx.compose.material3.RadioButtonDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
"""

if "import androidx.compose.material.icons.filled.NotificationsActive" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Add", imports.strip() + "\nimport androidx.compose.material.icons.filled.Add")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Clean build fixes applied.")

