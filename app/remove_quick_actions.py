import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Remove the item { QuickActionsStrip(...) } block inside Dashboard
pattern = r'item\s*\{\s*QuickActionsStrip\s*\(.*?\)\s*\}'
content = re.sub(pattern, '', content, flags=re.DOTALL)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

