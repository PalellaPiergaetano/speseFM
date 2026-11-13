import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix the missing `}` for `else { Scaffold(`
# We need to insert a `}` right before `@Composable\nprivate fun Dashboard(`
if "private fun Dashboard" in content:
    content = content.replace("}\n\n@Composable\nprivate fun Dashboard(", "}\n}\n\n@Composable\nprivate fun Dashboard(")

# Let's fix missing imports in MainActivity.kt
imports = """
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.HelpOutline
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.Switch
import androidx.compose.material3.RadioButton
import androidx.compose.material3.RadioButtonDefaults
"""
if "import androidx.compose.material.icons.automirrored.filled.ArrowBack" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Add", imports.strip() + "\nimport androidx.compose.material.icons.filled.Add")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

