import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("onClick = { onExpenseClick(e) }", "onClick = { onExpenseClick(it) }")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

