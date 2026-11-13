import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update loadExpenses and saveExpenses to persist date, time, and description
old_load_save = """private fun loadExpenses(context: Context): List<Expense> {
    val prefs = context.getSharedPreferences(ExpenseStore, 0)
    if (!prefs.contains("items")) return emptyList()
    val raw = prefs.getString("items", "") ?: ""
    if (raw.isBlank()) return emptyList()
    return raw.lines().mapNotNull { line ->
        val parts = line.split("\t")
        if (parts.size >= 3) {
            val title = parts[0]
            val category = parts[1]
            val amount = parseAmount(parts[2]) ?: return@mapNotNull null
            val month = if (parts.size >= 4) parts[3] else "settembre 26"
            Expense(title, category, amount, month)
        } else null
    }
}

private fun saveExpenses(context: Context, expenses: List<Expense>) {
    val raw = expenses.joinToString("\n") { "${it.title}\t${it.category}\t${it.amount}\t${it.month}" }
    context.getSharedPreferences(ExpenseStore, 0).edit().putString("items", raw).apply()
}"""

new_load_save = """private fun loadExpenses(context: Context): List<Expense> {
    val prefs = context.getSharedPreferences(ExpenseStore, 0)
    if (!prefs.contains("items")) return emptyList()
    val raw = prefs.getString("items", "") ?: ""
    if (raw.isBlank()) return emptyList()
    return raw.lines().mapNotNull { line ->
        val parts = line.split("\t")
        if (parts.size >= 3) {
            val title = parts[0]
            val category = parts[1]
            val amount = parseAmount(parts[2]) ?: return@mapNotNull null
            val month = if (parts.size >= 4) parts[3] else "settembre 26"
            val date = if (parts.size >= 5) parts[4] else ""
            val time = if (parts.size >= 6) parts[5] else ""
            val description = if (parts.size >= 7) parts[6] else ""
            Expense(title, category, amount, month, date, time, description)
        } else null
    }
}

private fun saveExpenses(context: Context, expenses: List<Expense>) {
    val raw = expenses.joinToString("\n") { "${it.title}\t${it.category}\t${it.amount}\t${it.month}\t${it.date}\t${it.time}\t${it.description}" }
    context.getSharedPreferences(ExpenseStore, 0).edit().putString("items", raw).apply()
}"""

content = content.replace(old_load_save, new_load_save)

# 2. Update MonthSelectorStrip to use Surface(onClick = { ... }) so month selection fires reliably
old_month_strip = """private fun MonthSelectorStrip(
    availableMonths: List<String>,
    selectedMonth: String?,
    isDark: Boolean,
    onMonthSelect: (String?) -> Unit
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White

    LazyRow(
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        contentPadding = PaddingValues(horizontal = 2.dp)
    ) {
        item {
            val isAllSelected = selectedMonth.isNullOrBlank()
            Surface(
                color = if (isAllSelected) Terracotta else cardBg,
                shape = CircleShape,
                shadowElevation = if (isAllSelected) 3.dp else 1.dp,
                modifier = Modifier.clip(CircleShape).clickable { onMonthSelect(null) }
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 7.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Default.CalendarMonth,
                        contentDescription = null,
                        tint = if (isAllSelected) Color.White else Terracotta,
                        modifier = Modifier.size(14.dp)
                    )
                    Spacer(Modifier.width(6.dp))
                    Text(
                        AppStrings.get(AppStrings.tutti_i_mesi, LocalAppLanguage.current),
                        color = if (isAllSelected) Color.White else textColor,
                        fontWeight = if (isAllSelected) FontWeight.Bold else FontWeight.Medium,
                        fontSize = 12.sp
                    )
                }
            }
        }

        items(availableMonths) { monthName ->
            val isSelected = selectedMonth?.equals(monthName, ignoreCase = true) == true
            Surface(
                color = if (isSelected) Terracotta else cardBg,
                shape = CircleShape,
                shadowElevation = if (isSelected) 3.dp else 1.dp,
                modifier = Modifier.clip(CircleShape).clickable { onMonthSelect(monthName) }
            ) {
                Text(
                    AppStrings.translateMonth(monthName, LocalAppLanguage.current),
                    color = if (isSelected) Color.White else textColor,
                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                    fontSize = 12.sp,
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 7.dp)
                )
            }
        }
    }
}"""

new_month_strip = """private fun MonthSelectorStrip(
    availableMonths: List<String>,
    selectedMonth: String?,
    isDark: Boolean,
    onMonthSelect: (String?) -> Unit
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White

    LazyRow(
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        contentPadding = PaddingValues(horizontal = 2.dp)
    ) {
        item {
            val isAllSelected = selectedMonth.isNullOrBlank()
            Surface(
                onClick = { onMonthSelect(null) },
                color = if (isAllSelected) Terracotta else cardBg,
                shape = CircleShape,
                shadowElevation = if (isAllSelected) 3.dp else 1.dp
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 7.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Default.CalendarMonth,
                        contentDescription = null,
                        tint = if (isAllSelected) Color.White else Terracotta,
                        modifier = Modifier.size(14.dp)
                    )
                    Spacer(Modifier.width(6.dp))
                    Text(
                        AppStrings.get(AppStrings.tutti_i_mesi, LocalAppLanguage.current),
                        color = if (isAllSelected) Color.White else textColor,
                        fontWeight = if (isAllSelected) FontWeight.Bold else FontWeight.Medium,
                        fontSize = 12.sp
                    )
                }
            }
        }

        items(availableMonths) { monthName ->
            val isSelected = selectedMonth?.equals(monthName, ignoreCase = true) == true
            Surface(
                onClick = { 
                    if (isSelected) onMonthSelect(null) else onMonthSelect(monthName)
                },
                color = if (isSelected) Terracotta else cardBg,
                shape = CircleShape,
                shadowElevation = if (isSelected) 3.dp else 1.dp
            ) {
                Text(
                    AppStrings.translateMonth(monthName, LocalAppLanguage.current),
                    color = if (isSelected) Color.White else textColor,
                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                    fontSize = 12.sp,
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 7.dp)
                )
            }
        }
    }
}"""

content = content.replace(old_month_strip, new_month_strip)

# 3. Update ExpenseRow tag to display expense.date if available, otherwise expense.month
old_row_month_tag = """                    if (expense.month.isNotBlank()) {
                        Spacer(Modifier.width(6.dp))
                        Text(
                            text = "• ${AppStrings.translateMonth(expense.month, LocalAppLanguage.current)}", 
                            color = Sage,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Medium,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }"""

new_row_month_tag = """                    val displayDate = if (expense.date.isNotBlank()) expense.date else expense.month
                    if (displayDate.isNotBlank()) {
                        Spacer(Modifier.width(6.dp))
                        Text(
                            text = "• ${AppStrings.translateMonth(displayDate, LocalAppLanguage.current)}", 
                            color = Sage,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Medium,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }"""

content = content.replace(old_row_month_tag, new_row_month_tag)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Month selection and real date persistence fixes applied successfully.")

