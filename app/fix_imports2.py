with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("package it.fm.spese\n\nimport androidx.compose.runtime.staticCompositionLocalOf\n\nval LocalAppLanguage = staticCompositionLocalOf { AppLanguage.ITALIAN }\n", "package it.fm.spese\n")

# Aggiungo alla fine degli import.
# Cerco l'ultimo import e aggiungo lì.
lines = content.split('\n')
last_import = 0
for i, line in enumerate(lines):
    if line.startswith("import "):
        last_import = i

lines.insert(last_import + 1, "import androidx.compose.runtime.staticCompositionLocalOf\n\nval LocalAppLanguage = staticCompositionLocalOf { AppLanguage.ITALIAN }\n")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write('\n'.join(lines))

