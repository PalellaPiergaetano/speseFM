import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# I removed it globally! `content = content.replace("val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)", "")`
# So Dashboard doesn't have it anymore.
# Let's put it back in Dashboard. Dashboard signature:
dashboard_sig = "modifier: Modifier\n) {"
content = content.replace(dashboard_sig, dashboard_sig + "\n    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

