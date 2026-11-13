import re
import json

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Trova tutte le stringhe "statiche" (senza $)
static_matches = re.findall(r'Text\(\s*"([^"$]+)"', content)
# Trova label
static_matches += re.findall(r'label = \{ Text\("([^"$]+)"\) \}', content)
# Trova toast statici
static_matches += re.findall(r'Toast\.makeText\(context,\s*"([^"$]+)"', content)

unique_strings = list(set(static_matches))
unique_strings = [s for s in unique_strings if s]

translations = {}
for i, s in enumerate(sorted(unique_strings)):
    key = re.sub(r'[^a-zA-Z0-9]', '_', s.lower())
    key = re.sub(r'_+', '_', key).strip('_')
    if not key: key = f"string_{i}"
    
    translations[key] = {
        "it": s,
        "en": s + " (EN)",
        "fr": s + " (FR)",
        "es": s + " (ES)",
    }

# AppStrings.kt content
kt_code = "package it.fm.spese\n\nobject AppStrings {\n"
for key, trans in translations.items():
    kt_code += f"    val {key} = mapOf(\n"
    kt_code += f'        AppLanguage.ITALIAN to "{trans["it"]}",\n'
    kt_code += f'        AppLanguage.ENGLISH to "{trans["en"]}",\n'
    kt_code += f'        AppLanguage.FRENCH to "{trans["fr"]}",\n'
    kt_code += f'        AppLanguage.SPANISH to "{trans["es"]}"\n'
    kt_code += f"    )\n"

kt_code += "\n    fun get(map: Map<AppLanguage, String>, lang: AppLanguage): String = map[lang] ?: map[AppLanguage.ITALIAN]!!\n}\n"

with open("src/main/java/it/fm/spese/AppStrings.kt", "w") as f:
    f.write(kt_code)

# Sostituzioni in MainActivity.kt
for key, trans in translations.items():
    original = f'Text("{trans["it"]}"'
    replacement = f'Text(AppStrings.get(AppStrings.{key}, appLanguage)'
    content = content.replace(original, replacement)
    
    original_2 = f'Text(text = "{trans["it"]}"'
    replacement_2 = f'Text(text = AppStrings.get(AppStrings.{key}, appLanguage)'
    content = content.replace(original_2, replacement_2)
    
    original_3 = f'Toast.makeText(context, "{trans["it"]}"'
    replacement_3 = f'Toast.makeText(context, AppStrings.get(AppStrings.{key}, appLanguage)'
    content = content.replace(original_3, replacement_3)
    
    original_4 = f'label = {{ Text("{trans["it"]}") }}'
    replacement_4 = f'label = {{ Text(AppStrings.get(AppStrings.{key}, appLanguage)) }}'
    content = content.replace(original_4, replacement_4)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

