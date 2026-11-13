import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

imports = "import androidx.compose.material.icons.filled.Info\n"
if "import androidx.compose.material.icons.filled.Info" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Add", imports + "import androidx.compose.material.icons.filled.Add")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

