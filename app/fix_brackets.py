import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# I see a top level declaration error at 940: `    if (showAddDialog) {`
# This means we closed the `fun SpeseApp()` too early.
# Let's count braces or just see what I replaced.
# In fix_applanguage.py, I did:
# content = content.replace("    if (showAddDialog) {\n        AddExpenseDialog(", "    }\n    if (showAddDialog) {\n        AddExpenseDialog(")
# This added an extra closing brace!

content = content.replace(
"""    }
    if (showAddDialog) {
        AddExpenseDialog(""",
"""    if (showAddDialog) {
        AddExpenseDialog(""")

# Actually, ModalNavigationDrawer needs to be closed at the very end of SpeseApp.
# `SpeseApp` ends before `data class TutorialStep`.
# Let's see if the extra `}` I added at the end of SpeseApp (with close_brace.py) matches the ones I opened.
# I opened:
# `androidx.compose.runtime.CompositionLocalProvider(...) {`
# `androidx.compose.material3.ModalNavigationDrawer(...) {`
# So I need 2 closing braces at the end of `SpeseApp`.
# Let's check `data class TutorialStep` in content.
idx = content.find("data class TutorialStep")
if idx != -1:
    # Get the text before it
    before = content[idx-50:idx]
    print(before)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

