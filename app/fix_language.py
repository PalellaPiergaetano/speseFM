import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Trova SpeseApp
# Sostituisci Icon(Icons.Default.Menu) con Icon(Icons.Default.Settings)
content = content.replace("Icon(Icons.Default.Menu, contentDescription = \"Menu\", tint = textColor)", "Icon(androidx.compose.material.icons.Icons.Default.Settings, contentDescription = \"Impostazioni\", tint = textColor)")

# Fix per LocalAppLanguage
# Se var appLanguage viene aggiornato ma la composizione non rileva il cambio del LocalAppLanguage,
# dobbiamo assicurarci che il CompositionLocalProvider sia posizionato dove può reagire al cambio di stato di appLanguage.
# Il CompositionLocalProvider era stato inserito dentro il Drawer? O in SpeseAppWithSecurity?
# Troviamo "CompositionLocalProvider("
lines = content.split('\n')
for i, line in enumerate(lines):
    if "CompositionLocalProvider(" in line:
        pass
        
with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

