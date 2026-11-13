import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.material3.NavigationBar\n", "import androidx.compose.material3.NavigationBar\nimport androidx.compose.material3.ExperimentalMaterial3Api\n")
content = content.replace("@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\n", "@OptIn(ExperimentalMaterial3Api::class)\n")

# OptIn the whole file
content = content.replace("package it.fm.spese\n", "package it.fm.spese\n\n@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\n")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

