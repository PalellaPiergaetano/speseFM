import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix `appLang` not changing.
# In `SpeseAppWithSecurity`:
#    val appLang = loadAppLanguage(LocalContext.current)
# This isn't a state! It's just evaluated once.
# We need to use `var appLang by remember { mutableStateOf(loadAppLanguage(context)) }`

content = content.replace(
"""        val appLang = loadAppLanguage(LocalContext.current)
        androidx.compose.runtime.CompositionLocalProvider(LocalAppLanguage provides appLang) {""",
"""        val context = LocalContext.current
        var appLang by remember { mutableStateOf(loadAppLanguage(context)) }
        androidx.compose.runtime.CompositionLocalProvider(LocalAppLanguage provides appLang) {""")

# In `LanguageSettingsDialog` we had `onSelectLanguage = { lang -> ... }`
# We passed `currentLanguage = loadAppLanguage(context)` but didn't pass `onLangChanged` callback.
# `SpeseApp` needs to accept `onLangChanged: (AppLanguage) -> Unit` so it can update `appLang` in `SpeseAppWithSecurity`.

content = content.replace(
"""private fun SpeseApp(
    onLockClick: () -> Unit,
    launchImport: (((Uri?) -> Unit) -> Unit),
    launchExport: ((String, (Uri?) -> Unit) -> Unit)
) {""",
"""private fun SpeseApp(
    onLockClick: () -> Unit,
    launchImport: (((Uri?) -> Unit) -> Unit),
    launchExport: ((String, (Uri?) -> Unit) -> Unit),
    onLangChanged: (AppLanguage) -> Unit
) {""")

content = content.replace(
"""            SpeseApp(
                onLockClick = { isUnlocked = false },
                launchImport = launchImport,
                launchExport = launchExport
            )""",
"""            SpeseApp(
                onLockClick = { isUnlocked = false },
                launchImport = launchImport,
                launchExport = launchExport,
                onLangChanged = { lang -> appLang = lang }
            )""")

content = content.replace(
"""        LanguageSettingsDialog(
            currentLanguage = loadAppLanguage(context),
            isDarkTheme = isDarkTheme,
            onDismiss = { showSettingsDialog = false },
            onSelectLanguage = { lang -> 
                saveAppLanguage(context, lang)
                Toast.makeText(context, "Lingua aggiornata. Riavvia l'app.", Toast.LENGTH_SHORT).show()
                showSettingsDialog = false
            }
        )""",
"""        LanguageSettingsDialog(
            currentLanguage = LocalAppLanguage.current,
            isDarkTheme = isDarkTheme,
            onDismiss = { showSettingsDialog = false },
            onSelectLanguage = { lang -> 
                saveAppLanguage(context, lang)
                onLangChanged(lang)
                showSettingsDialog = false
            }
        )""")


with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

