import re

with open("src/main/java/it/fm/spese/AppStrings.kt", "r") as f:
    content = f.read()

content = content.replace("altra(ES)", "Altro (ES)")

with open("src/main/java/it/fm/spese/AppStrings.kt", "w") as f:
    f.write(content)

