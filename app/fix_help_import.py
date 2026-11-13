import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.material.icons.automirrored.filled.HelpOutline", "")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

