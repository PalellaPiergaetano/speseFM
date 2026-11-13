import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add states in SpeseApp
content = content.replace("var showAddDialog by remember { mutableStateOf(false) }", "var showAddDialog by remember { mutableStateOf(false) }\n    var showRemindersDialog by remember { mutableStateOf(false) }\n    var showSettingsDialog by remember { mutableStateOf(false) }\n    var showClearConfirmDialog by remember { mutableStateOf(false) }")

# Fix onTogglePrivacy
content = content.replace("onTogglePrivacy()", "isPrivacyMode = !isPrivacyMode; savePrivacyMode(context, isPrivacyMode); Toast.makeText(context, if (isPrivacyMode) \"Privacy attivata\" else \"Privacy disattivata\", Toast.LENGTH_SHORT).show()")

# Conflicting declarations
lines = content.split('\n')
for i in range(len(lines)):
    if "val textColor =" in lines[i] and "val textColor =" in lines[i+1]:
        lines[i] = ""

# I also need to find Conflicting declarations around line 2593 and 2606.
# They might not be on consecutive lines.
for i in range(len(lines)):
    if "Conflicting declarations" in lines[i]: pass

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write('\n'.join(lines).replace("val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)\n    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)", "val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)"))

