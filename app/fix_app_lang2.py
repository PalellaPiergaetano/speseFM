import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# I see a bunch of `Unresolved reference 'LocalAppLanguage'`.
# This is because I put `val LocalAppLanguage` inside `fun MainActivity` or something?
# Let's see where `LocalAppLanguage` is defined.
lines = content.split('\n')
for i, line in enumerate(lines):
    if "val LocalAppLanguage" in line:
        print(f"Line {i}: {line}")

# Also missing `import androidx.compose.runtime.staticCompositionLocalOf`
