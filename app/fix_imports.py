with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.runtime.staticCompositionLocalOf\n\nval LocalAppLanguage = staticCompositionLocalOf { AppLanguage.ITALIAN }\n\n", "")

# Add it at the top after package
content = content.replace("package it.fm.spese\n", "package it.fm.spese\n\nimport androidx.compose.runtime.staticCompositionLocalOf\n\nval LocalAppLanguage = staticCompositionLocalOf { AppLanguage.ITALIAN }\n")

# Wrap Scaffold with CompositionLocalProvider(LocalAppLanguage provides appLanguage)
# It's at SpeseApp Scaffold. Let's find "Scaffold(" and replace if it's SpeseApp.
# Actually, wait. I will just do it manually with a python regex.

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

