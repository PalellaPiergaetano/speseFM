import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add appLanguage to SpeseApp
content = content.replace("var showSettingsDialog by remember { mutableStateOf(false) }", "var showSettingsDialog by remember { mutableStateOf(false) }\n    var appLanguage by remember { mutableStateOf(loadAppLanguage(context)) }")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

