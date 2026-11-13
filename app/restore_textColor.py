import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Trova tutti i "isDark: Boolean" e aggiunge "val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)"
# Wait, some have isDarkTheme: Boolean.
# I will use a regex to find all composables that use `textColor` but don't define it.
lines = content.split('\n')
for i in range(len(lines)):
    if "isDark: Boolean" in lines[i] or "isDarkTheme: Boolean" in lines[i]:
        # Look ahead for opening brace
        for j in range(i, min(i+15, len(lines))):
            if ") {" in lines[j] or "{" in lines[j]:
                # Insert textColor definition inside the block
                var_name = "isDark" if "isDark: Boolean" in lines[i] else "isDarkTheme"
                # Check if it already has it
                has_it = False
                for k in range(j, min(j+10, len(lines))):
                    if "val textColor =" in lines[k]:
                        has_it = True
                if not has_it:
                    lines.insert(j+1, f"    val textColor = if ({var_name}) Color(0xFFF3EFEA) else Color(0xFF1E1B18)")
                break

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write('\n'.join(lines))

