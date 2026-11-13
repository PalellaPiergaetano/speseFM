import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Replace hardcoded strings with AppStrings

with open("src/main/java/it/fm/spese/AppStrings.kt", "r") as f:
    app_strings = f.read()

keys_and_values = {}
matches = re.findall(r'val ([a-zA-Z0-9_]+) = mapOf\(\s*AppLanguage\.ITALIAN to "([^"]+)"', app_strings)
for key, value in matches:
    keys_and_values[value] = key

for val_it, key in keys_and_values.items():
    content = content.replace(f'Text("{val_it}"', f'Text(AppStrings.get(AppStrings.{key}, LocalAppLanguage.current)')
    content = content.replace(f'Text(text = "{val_it}"', f'Text(text = AppStrings.get(AppStrings.{key}, LocalAppLanguage.current)')
    content = content.replace(f'Toast.makeText(context, "{val_it}"', f'Toast.makeText(context, AppStrings.get(AppStrings.{key}, LocalAppLanguage.current)')
    content = content.replace(f'label = {{ Text("{val_it}") }}', f'label = {{ Text(AppStrings.get(AppStrings.{key}, LocalAppLanguage.current)) }}')

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

