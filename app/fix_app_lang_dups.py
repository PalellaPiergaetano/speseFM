import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Replace any occurrence of two consecutive `val appLang = LocalAppLanguage.current` with just one
while "val appLang = LocalAppLanguage.current\n    val appLang = LocalAppLanguage.current" in content:
    content = content.replace("val appLang = LocalAppLanguage.current\n    val appLang = LocalAppLanguage.current", "val appLang = LocalAppLanguage.current")

while "val appLang = LocalAppLanguage.current\n    val appLang = LocalAppLanguage.current" in content.replace("    ", ""):
    # general cleanup
    pass

# Let's use regex to find and remove duplicate `val appLang = LocalAppLanguage.current` inside the same function body
def clean_dups(match):
    return "val appLang = LocalAppLanguage.current"

# Actually, let's just replace all `val appLang = LocalAppLanguage.current` inside `SettingsScreen`, `ExpenseDetailScreen`, `LanguageSettingsDialog`, `RemindersScreen`, `ReminderCard`, `AddReminderDialog` if they already have it.
content = content.replace("    val appLang = LocalAppLanguage.current\n    val appLang = LocalAppLanguage.current", "    val appLang = LocalAppLanguage.current")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

