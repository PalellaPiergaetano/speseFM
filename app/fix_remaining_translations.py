import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. MonthSelectorStrip "Tutti i Mesi"
content = content.replace(
    'Text(\n                        "Tutti i Mesi",',
    'val appLang = LocalAppLanguage.current\n                    Text(\n                        AppStrings.get(AppStrings.tutti_i_mesi, appLang),'
)

# 2. "Categorie principali"
content = content.replace(
    'Text("Categorie principali", color = textColor',
    'val appLang = LocalAppLanguage.current\n            Text(AppStrings.get(AppStrings.categorie_principali, appLang), color = textColor'
)

# 3. "Vedi tutte"
content = content.replace(
    'Text(\n                    "Vedi tutte",',
    'val appLang = LocalAppLanguage.current\n                    Text(\n                        AppStrings.get(AppStrings.vedi_tutte, appLang),'
)

# 4. "Suggerimento Intelligente"
content = content.replace(
    'Text("Suggerimento Intelligente", color = textColor',
    'val appLang = LocalAppLanguage.current\n            Text(AppStrings.get(AppStrings.suggerimento_intelligente, appLang), color = textColor'
)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Remaining translations fixed.")

