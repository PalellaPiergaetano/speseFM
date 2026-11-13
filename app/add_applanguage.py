import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add AppLanguage after colors
# Find "private val Violet = Color(0xFF6C5CE7)"
injection = """
enum class AppLanguage(val code: String, val displayName: String, val flag: String) {
    ITALIAN("it", "Italiano", "🇮🇹"),
    ENGLISH("en", "English", "🇬🇧"),
    FRENCH("fr", "Français", "🇫🇷"),
    SPANISH("es", "Español", "🇪🇸")
}

val LocalAppLanguage = androidx.compose.runtime.staticCompositionLocalOf { AppLanguage.ITALIAN }

"""

content = content.replace("private val Violet = Color(0xFF6C5CE7)\n", "private val Violet = Color(0xFF6C5CE7)\n" + injection)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

