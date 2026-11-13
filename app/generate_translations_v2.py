import re
import json

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Already generated AppStrings.kt, so we just use the existing one to do replacements
import importlib.util
# Actually, I'll just regenerate the replacements based on the strings I find.
# Or better, just parse AppStrings.kt!
with open("src/main/java/it/fm/spese/AppStrings.kt", "r") as f:
    app_strings = f.read()

keys_and_values = {}
# val string_1 = mapOf( ... ITALIAN to "Annulla"
matches = re.findall(r'val ([a-zA-Z0-9_]+) = mapOf\(\s*AppLanguage\.ITALIAN to "([^"]+)"', app_strings)
for key, value in matches:
    keys_and_values[value] = key

# Now replace in MainActivity.kt
for val_it, key in keys_and_values.items():
    # Only replace if it's not already using AppStrings
    
    # 1. Text("...") -> Text(AppStrings.get(AppStrings.key, LocalAppLanguage.current)
    content = content.replace(f'Text("{val_it}"', f'Text(AppStrings.get(AppStrings.{key}, LocalAppLanguage.current)')
    
    # 2. Text(text = "...") -> Text(text = AppStrings.get(...)
    content = content.replace(f'Text(text = "{val_it}"', f'Text(text = AppStrings.get(AppStrings.{key}, LocalAppLanguage.current)')
    
    # 3. Toast.makeText(context, "...") -> Here we can't use LocalAppLanguage.current easily if it's outside composition.
    # Actually, we can just use `appLanguage` if it's available, or `AppLanguage.ITALIAN`.
    # Let's replace with `AppLanguage.ITALIAN` for Toast for now to avoid compilation errors, 
    # since Toast internationalization is less critical or can be fixed manually.
    content = content.replace(f'Toast.makeText(context, "{val_it}"', f'Toast.makeText(context, AppStrings.get(AppStrings.{key}, AppLanguage.ITALIAN)')
    
    # 4. label = { Text("...") }
    content = content.replace(f'label = {{ Text("{val_it}") }}', f'label = {{ Text(AppStrings.get(AppStrings.{key}, LocalAppLanguage.current)) }}')

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

