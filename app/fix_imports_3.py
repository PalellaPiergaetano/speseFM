with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

lines = content.split('\n')
last_import = 0
for i, line in enumerate(lines):
    if line.startswith("import "):
        last_import = i

lines.insert(last_import + 1, "import kotlinx.coroutines.launch")
lines.insert(last_import + 1, "import androidx.compose.material.icons.filled.Notifications")
lines.insert(last_import + 1, "import androidx.compose.material.icons.filled.Language")
lines.insert(last_import + 1, "import androidx.compose.material.icons.filled.Lock")
lines.insert(last_import + 1, "import androidx.compose.material.icons.filled.FileUpload")
lines.insert(last_import + 1, "import androidx.compose.material.icons.filled.FileDownload")
lines.insert(last_import + 1, "import androidx.compose.material.icons.filled.Help")
lines.insert(last_import + 1, "import androidx.compose.material.icons.filled.Delete")
lines.insert(last_import + 1, "import androidx.compose.material.icons.filled.Menu")

# Replace kotlinx.coroutines.launch back to scope.launch
new_content = '\n'.join(lines).replace("kotlinx.coroutines.launch", "scope.launch")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(new_content)

