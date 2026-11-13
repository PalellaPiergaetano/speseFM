import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. MonthSelectorStrip item rendering
old_month_text = """                Text(
                    monthName,
                    color = if (isSelected) Color.White else textColor,
                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                    fontSize = 12.sp
                )"""

new_month_text = """                Text(
                    AppStrings.translateMonth(monthName, LocalAppLanguage.current),
                    color = if (isSelected) Color.White else textColor,
                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                    fontSize = 12.sp
                )"""

content = content.replace(old_month_text, new_month_text)

# 2. CategoryQuickStrip rendering
old_cat_text = """                Text(
                    category,
                    color = textColor,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold
                )"""

new_cat_text = """                Text(
                    AppStrings.translateCategory(category, LocalAppLanguage.current),
                    color = textColor,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold
                )"""

content = content.replace(old_cat_text, new_cat_text)

# 3. ExpenseRow rendering for category and month
old_row_subtext = """                Text(
                    text = "${expense.category} • ${expense.month}",
                    color = subTextColor,
                    fontSize = 11.sp
                )"""

new_row_subtext = """                Text(
                    text = "${AppStrings.translateCategory(expense.category, appLang)} • ${AppStrings.translateMonth(expense.month, appLang)}",
                    color = subTextColor,
                    fontSize = 11.sp
                )"""

content = content.replace(old_row_subtext, new_row_subtext)

# 4. ExpenseDetailScreen category and month rows
content = content.replace(
    'DetailRow(AppStrings.get(AppStrings.categoria, appLang), expense.category, textColor, subTextColor)',
    'DetailRow(AppStrings.get(AppStrings.categoria, appLang), AppStrings.translateCategory(expense.category, appLang), textColor, subTextColor)'
)

content = content.replace(
    'DetailRow(AppStrings.get(AppStrings.mese, appLang), expense.month, textColor, subTextColor)',
    'DetailRow(AppStrings.get(AppStrings.mese, appLang), AppStrings.translateMonth(expense.month, appLang), textColor, subTextColor)'
)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Category and Month localization applied to MainActivity.kt.")

