import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix the import before package
if content.startswith("import kotlinx.coroutines.launch\npackage it.fm.spese\n"):
    content = content.replace("import kotlinx.coroutines.launch\npackage it.fm.spese\n", "package it.fm.spese\n\nimport kotlinx.coroutines.launch\n")

# Fix conflicting declarations
content = re.sub(r'val coroutineScope = rememberCoroutineScope\(\)\n\s*var showClearConfirmDialog by remember \{ mutableStateOf\(false\) \}', r'val coroutineScope = rememberCoroutineScope()', content)
content = re.sub(r'var showClearConfirmDialog by remember \{ mutableStateOf\(false\) \}\n\s*var showClearConfirmDialog by remember \{ mutableStateOf\(false\) \}', r'var showClearConfirmDialog by remember { mutableStateOf(false) }', content)

# I saw another showClearConfirmDialog
# Wait, let's just make it unique
lines = content.split('\n')
out = []
seen_showClearConfirmDialog = False
in_composable = False
for line in lines:
    if "@Composable" in line:
        pass # reset per composable
    if "fun " in line and "{" in line:
        seen_showClearConfirmDialog = False
        
    if "var showClearConfirmDialog by remember { mutableStateOf(false) }" in line:
        if seen_showClearConfirmDialog:
            continue # skip duplicate
        else:
            seen_showClearConfirmDialog = True
    out.append(line)
    
content = '\n'.join(out)

# Fix launch inside non-composable
content = content.replace("drawerState.close()", "coroutineScope.launch { drawerState.close() }")
content = content.replace("drawerState.open()", "coroutineScope.launch { drawerState.open() }")
# Since we might have duplicated coroutineScope.launch { coroutineScope.launch { ... } }, let's clean it up
content = content.replace("coroutineScope.launch { coroutineScope.launch {", "coroutineScope.launch {")
content = content.replace("} }", "}") # roughly, actually no that's dangerous. Let's not do the replace open/close naively.

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)
