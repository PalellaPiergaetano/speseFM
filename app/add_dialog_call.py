import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

injection = """
    if (showSettingsDialog) {
        LanguageSettingsDialog(
            currentLanguage = appLanguage,
            isDarkTheme = isDarkTheme,
            onDismiss = { showSettingsDialog = false },
            onSelectLanguage = { lang -> 
                appLanguage = lang
                saveAppLanguage(context, lang)
                Toast.makeText(context, "Lingua aggiornata", Toast.LENGTH_SHORT).show()
                showSettingsDialog = false
            }
        )
    }
"""

content = content.replace("if (showAddDialog)", injection + "\n    if (showAddDialog)")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

