import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add val appLang = LocalAppLanguage.current at the top of SpeseApp
target = """private fun SpeseApp(
    onOpenLanguageDialog: () -> Unit,
    onLockClick: () -> Unit,
    launchImport: (((Uri?) -> Unit) -> Unit),
    launchExport: ((String, (Uri?) -> Unit) -> Unit)
) {
    val context = LocalContext.current"""

replacement = """private fun SpeseApp(
    onOpenLanguageDialog: () -> Unit,
    onLockClick: () -> Unit,
    launchImport: (((Uri?) -> Unit) -> Unit),
    launchExport: ((String, (Uri?) -> Unit) -> Unit)
) {
    val context = LocalContext.current
    val appLang = LocalAppLanguage.current"""

content = content.replace(target, replacement)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

