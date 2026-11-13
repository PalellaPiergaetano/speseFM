import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix extra closing brace after SettingsScreen
content = content.replace("        }\n    }\n    }\n}\n\n\n@Composable\nfun SettingsItemRow(", "        }\n    }\n}\n\n\n@Composable\nfun SettingsItemRow(")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

