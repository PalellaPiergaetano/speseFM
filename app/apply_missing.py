import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add states in SpeseApp
content = content.replace("var showAddDialog by remember { mutableStateOf(false) }", "var showAddDialog by remember { mutableStateOf(false) }\n    var showRemindersDialog by remember { mutableStateOf(false) }\n    var showSettingsDialog by remember { mutableStateOf(false) }\n    var showClearConfirmDialog by remember { mutableStateOf(false) }")

content = content.replace("""    if (showAddDialog) {""", """    if (showSettingsDialog) {
        LanguageSettingsDialog(
            currentLanguage = loadAppLanguage(context),
            isDarkTheme = isDarkTheme,
            onDismiss = { showSettingsDialog = false },
            onSelectLanguage = { lang -> 
                saveAppLanguage(context, lang)
                Toast.makeText(context, "Lingua aggiornata. Riavvia l'app.", Toast.LENGTH_SHORT).show()
                showSettingsDialog = false
            }
        )
    }
    if (showAddDialog) {""")

content = content.replace("""    if (showClearConfirmDialog) {""", """    if (showClearConfirmDialog) {""") # It's already there

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

