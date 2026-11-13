import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Add import
if "import androidx.activity.compose.BackHandler" not in content:
    content = content.replace(
        "import androidx.activity.compose.setContent",
        "import androidx.activity.compose.BackHandler\nimport androidx.activity.compose.setContent"
    )

# 2. Add BackHandler in SpeseApp
old_routing = """                if (selectedExpense != null) {
                    ExpenseDetailScreen("""

new_routing = """                if (selectedExpense != null) {
                    BackHandler { selectedExpense = null }
                    ExpenseDetailScreen("""

content = content.replace(old_routing, new_routing)

old_reminders_route = """                } else if (showRemindersScreen) {
                    RemindersScreen("""

new_reminders_route = """                } else if (showRemindersScreen) {
                    BackHandler { showRemindersScreen = false }
                    RemindersScreen("""

content = content.replace(old_reminders_route, new_reminders_route)

old_settings_route = """                } else if (showSettings) {
                    SettingsScreen("""

new_settings_route = """                } else if (showSettings) {
                    BackHandler { showSettings = false }
                    SettingsScreen("""

content = content.replace(old_settings_route, new_settings_route)

# Add BackHandler when on non-home tabs (selectedTab != 0)
old_scaffold_route = """                } else {
                Scaffold("""

new_scaffold_route = """                } else {
                    if (selectedTab != 0) {
                        BackHandler { selectedTab = 0 }
                    }
                Scaffold("""

content = content.replace(old_scaffold_route, new_scaffold_route)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("BackHandler added successfully.")

