import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Let's remove QuickActionsStrip from Dashboard
content = re.sub(r'item\s*\{\s*QuickActionsStrip\(.*?\)\s*\}', '', content, flags=re.DOTALL)

# Add appLang to Dashboard
if "val appLang = LocalAppLanguage.current" not in content and "fun Dashboard" in content:
    content = content.replace("val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)", "val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)\n    val appLang = LocalAppLanguage.current")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

