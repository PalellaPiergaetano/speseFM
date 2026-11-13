import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

imports = """
import androidx.compose.material.icons.filled.NotificationsActive
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
"""

if "import androidx.compose.material.icons.filled.NotificationsActive" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Add", imports.strip() + "\nimport androidx.compose.material.icons.filled.Add")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

