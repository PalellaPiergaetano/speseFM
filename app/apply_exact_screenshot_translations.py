import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. MonthSelectorStrip fixes
content = content.replace(
    'Text(\n                        "Tutti i Mesi",',
    'Text(\n                        AppStrings.get(AppStrings.tutti_i_mesi, LocalAppLanguage.current),'
)

old_month_strip_item = """                Text(
                    monthName,
                    color = if (isSelected) Color.White else textColor,"""

new_month_strip_item = """                Text(
                    AppStrings.translateMonth(monthName, LocalAppLanguage.current),
                    color = if (isSelected) Color.White else textColor,"""

content = content.replace(old_month_strip_item, new_month_strip_item)

# 2. CategoryQuickStrip fixes
old_cat_strip_text = """                        Column {
                            Text(category, color = textColor, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)"""

new_cat_strip_text = """                        Column {
                            Text(AppStrings.translateCategory(category, LocalAppLanguage.current), color = textColor, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, maxLines = 1, overflow = TextOverflow.Ellipsis)"""

content = content.replace(old_cat_strip_text, new_cat_strip_text)

# 3. Movements (Transactions) filter bar fixes
content = content.replace(
    'Text(\n                            "Tutte le categorie",',
    'Text(\n                            AppStrings.get(AppStrings.tutte_le_categorie, LocalAppLanguage.current),'
)

old_mov_cat_filter_text = """                            Text(
                                category,
                                color = if (isSelected) Color.White else textColor,"""

new_mov_cat_filter_text = """                            Text(
                                AppStrings.translateCategory(category, LocalAppLanguage.current),
                                color = if (isSelected) Color.White else textColor,"""

content = content.replace(old_mov_cat_filter_text, new_mov_cat_filter_text)

# 4. ExpenseRow category and month tag fixes
old_row_cat_tag = """                        Text(
                            text = expense.category,"""

new_row_cat_tag = """                        Text(
                            text = AppStrings.translateCategory(expense.category, LocalAppLanguage.current),"""

content = content.replace(old_row_cat_tag, new_row_cat_tag)

old_row_month_tag = """                        Text(
                            text = "• ${expense.month}", """

new_row_month_tag = """                        Text(
                            text = "• ${AppStrings.translateMonth(expense.month, LocalAppLanguage.current)}", """

content = content.replace(old_row_month_tag, new_row_month_tag)

# 5. Reports breakdown chart legend fixes
old_reports_legend_text = """                                    Text(
                                        category,
                                        color = textColor,"""

new_reports_legend_text = """                                    Text(
                                        AppStrings.translateCategory(category, LocalAppLanguage.current),
                                        color = textColor,"""

content = content.replace(old_reports_legend_text, new_reports_legend_text)

# 6. Donut chart center label fix
content = content.replace(
    'text = displayCategory ?: "Totale Mese"',
    'text = if (displayCategory != null) AppStrings.translateCategory(displayCategory, LocalAppLanguage.current) else AppStrings.get(AppStrings.totale_mese, LocalAppLanguage.current)'
)

# 7. Dashboard "Vedi tutte" button fix
content = content.replace(
    'Text(\n                        "Vedi tutte",',
    'Text(\n                        AppStrings.get(AppStrings.vedi_tutte, LocalAppLanguage.current),'
)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Exact screenshot translations applied successfully.")

