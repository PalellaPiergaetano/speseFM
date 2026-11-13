import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Trova tutti i Text("...")
matches = re.findall(r'Text\(\s*"([^"]+)"', content)
matches += re.findall(r'Toast\.makeText\(context,\s*"([^"]+)"', content)

# Unique
unique_strings = list(set(matches))
print("Found", len(unique_strings), "strings")
for s in sorted(unique_strings):
    print(f'"{s}"')

