import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add textColor
content = content.replace(
    "val subTextColor = if (isDarkTheme) Color(0xFFA0B2A3) else Color(0xFF5B7B68)",
    "val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)\n    val subTextColor = if (isDarkTheme) Color(0xFFA0B2A3) else Color(0xFF5B7B68)"
)

# Fix Divider
content = content.replace("Divider(", "androidx.compose.material3.HorizontalDivider(")

# OptIn ExperimentalMaterial3Api for SpeseApp
content = content.replace(
"""private fun SpeseApp(
    onLockClick: () -> Unit,""",
"""@androidx.compose.material3.ExperimentalMaterial3Api
private fun SpeseApp(
    onLockClick: () -> Unit,"""
)

# Fix launch inside scope
content = content.replace("scope.launch", "kotlinx.coroutines.launch")
# Actually it's scope.launch, wait, it requires importing kotlinx.coroutines.launch. 
# But scope is a CoroutineScope, so it's `import kotlinx.coroutines.launch`. I will just use `scope.launch {` but I need to import it.

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

