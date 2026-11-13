import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix @file:OptIn location
# Kotlin requires @file: annotations before package definition
content = content.replace("package it.fm.spese\n\n@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\n", "@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)\npackage it.fm.spese\n\n")

# Remove duplicate imports
content = content.replace("import androidx.compose.material3.ExperimentalMaterial3Api\nimport androidx.compose.material3.ExperimentalMaterial3Api\n", "import androidx.compose.material3.ExperimentalMaterial3Api\n")
lines = content.split('\n')
for i in range(len(lines)):
    if "import androidx.compose.material3.ExperimentalMaterial3Api" in lines[i]:
        # just keep one, I'll let it be for now since I'm manually removing conflicting declarations
        pass
        
# Fix showClearConfirmDialog conflict
for i in range(len(lines)):
    if "var showClearConfirmDialog" in lines[i] and "var showClearConfirmDialog" in lines[i+1]:
        lines[i] = ""
    elif "var showClearConfirmDialog" in lines[i] and "var showClearConfirmDialog" in lines[i+2]:
        lines[i] = ""

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write('\n'.join(lines))

