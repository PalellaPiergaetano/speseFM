import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("Icons.Default.HelpOutline", "Icons.Default.Info")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

