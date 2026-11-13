import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Trovo `LocalAppLanguage provides appLanguage`
# Wait, I didn't see `LocalAppLanguage provides appLanguage` in my previous grep. That means I never wrapped `SpeseApp`!

wrapper = """
    androidx.compose.runtime.CompositionLocalProvider(LocalAppLanguage provides appLanguage) {
        androidx.compose.material3.ModalNavigationDrawer(
"""

content = content.replace("        androidx.compose.material3.ModalNavigationDrawer(", wrapper)

# Cerco la fine del ModalNavigationDrawer
# ModalNavigationDrawer starts around line 630.
# The whole SpeseApp function ends around line 1120.
content = content.replace(
"""    if (showAddDialog) {
        AddExpenseDialog(""",
"""    }
    if (showAddDialog) {
        AddExpenseDialog(""")


with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

