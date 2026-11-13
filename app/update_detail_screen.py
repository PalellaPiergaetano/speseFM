import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

old_details = """                    DetailRow(AppStrings.get(AppStrings.categoria, appLang), expense.category, textColor, subTextColor)
                    DetailRow(AppStrings.get(AppStrings.data, appLang), expense.date, textColor, subTextColor)
                    if (expense.time.isNotBlank()) {
                        DetailRow(AppStrings.get(AppStrings.ora, appLang), expense.time, textColor, subTextColor)
                    }
                    if (expense.description.isNotBlank()) {
                        DetailRow(AppStrings.get(AppStrings.descrizione, appLang), expense.description, textColor, subTextColor)
                    }"""

new_details = """                    DetailRow(AppStrings.get(AppStrings.categoria, appLang), expense.category, textColor, subTextColor)
                    DetailRow("Mese", expense.month, textColor, subTextColor)
                    if (expense.date.isNotBlank()) {
                        DetailRow(AppStrings.get(AppStrings.data, appLang), expense.date, textColor, subTextColor)
                    }
                    if (expense.time.isNotBlank()) {
                        DetailRow(AppStrings.get(AppStrings.ora, appLang), expense.time, textColor, subTextColor)
                    }
                    if (expense.description.isNotBlank()) {
                        DetailRow(AppStrings.get(AppStrings.descrizione, appLang), expense.description, textColor, subTextColor)
                    }"""

content = content.replace(old_details, new_details)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

