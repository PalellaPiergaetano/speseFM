import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix import scope.launch -> kotlinx.coroutines.launch
content = content.replace("import scope.launch", "import kotlinx.coroutines.launch")

# Fix conflicting textColor
# In SpeseApp, I might have added it twice?
# Let's see:
# I used: content = content.replace( "val subTextColor = ...", "val textColor = ...\n    val subTextColor = ...")
# So if textColor was already defined, now it's defined twice.
# I will use a regex to find duplicate `val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)`
matches = re.finditer(r'val textColor = if \(isDarkTheme\) Color\(0xFFF3EFEA\) else Color\(0xFF1E1B18\)', content)
indices = [m.start() for m in matches]
if len(indices) > 1:
    # Just remove the second one in Dashboard? No, line 991 is inside Dashboard!
    pass
    
# Actually, I can just fix it by replacing the duplicate in Dashboard.
# Dashboard starts around line 1146.
# I will just remove `val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)` inside Dashboard.
content = content.replace("val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)", "")

# Wait, the conflicting declaration was at 991 and 992. Let's see what is there.
lines = content.split('\n')
for i in range(len(lines)):
    if "val textColor =" in lines[i] and "val textColor =" in lines[i+1]:
        lines[i] = ""

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write('\n'.join(lines))

