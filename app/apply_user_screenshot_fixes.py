import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update ExposedDropdownMenu inside AddExpenseDialog to display translated category names
old_dropdown_val = """                        OutlinedTextField(
                            value = manualCategory,"""

new_dropdown_val = """                        OutlinedTextField(
                            value = AppStrings.translateCategory(manualCategory, LocalAppLanguage.current),"""

content = content.replace(old_dropdown_val, new_dropdown_val)

old_dropdown_item = """                                            Text(
                                                category,
                                                color = textColor,
                                                fontWeight = if (category == manualCategory) FontWeight.Bold else FontWeight.Normal
                                            )"""

new_dropdown_item = """                                            Text(
                                                AppStrings.translateCategory(category, LocalAppLanguage.current),
                                                color = textColor,
                                                fontWeight = if (category == manualCategory) FontWeight.Bold else FontWeight.Normal
                                            )"""

content = content.replace(old_dropdown_item, new_dropdown_item)

# 2. Add manual Date and Time input fields in AddExpenseDialog
old_manual_col = """                // INSERIMENTO MANUALE
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    OutlinedTextField(
                        value = manualTitle,"""

new_manual_col = """                // INSERIMENTO MANUALE
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    val appLang = LocalAppLanguage.current
                    var manualDate by remember { mutableStateOf(java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())) }
                    var manualTime by remember { mutableStateOf(java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())) }

                    OutlinedTextField(
                        value = manualTitle,"""

content = content.replace(old_manual_col, new_manual_col)

# Add Date and Time fields right after Amount field
old_amount_field = """                    OutlinedTextField(
                        value = manualAmount,
                        onValueChange = { manualAmount = it },
                        label = { Text(AppStrings.get(AppStrings.importo, LocalAppLanguage.current)) },
                        singleLine = true,
                        shape = RoundedCornerShape(16.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Terracotta,
                            focusedLabelColor = Terracotta,
                            focusedTextColor = textColor,
                            unfocusedTextColor = textColor
                        ),
                        modifier = Modifier.fillMaxWidth()
                    )"""

new_amount_field = """                    OutlinedTextField(
                        value = manualAmount,
                        onValueChange = { manualAmount = it },
                        label = { Text(AppStrings.get(AppStrings.importo, LocalAppLanguage.current)) },
                        singleLine = true,
                        shape = RoundedCornerShape(16.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Terracotta,
                            focusedLabelColor = Terracotta,
                            focusedTextColor = textColor,
                            unfocusedTextColor = textColor
                        ),
                        modifier = Modifier.fillMaxWidth()
                    )

                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        OutlinedTextField(
                            value = manualDate,
                            onValueChange = { manualDate = it },
                            label = { Text(AppStrings.get(AppStrings.data, appLang)) },
                            singleLine = true,
                            shape = RoundedCornerShape(16.dp),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = Terracotta,
                                focusedLabelColor = Terracotta,
                                focusedTextColor = textColor,
                                unfocusedTextColor = textColor
                            ),
                            modifier = Modifier.weight(1f)
                        )
                        OutlinedTextField(
                            value = manualTime,
                            onValueChange = { manualTime = it },
                            label = { Text(AppStrings.get(AppStrings.ora, appLang)) },
                            singleLine = true,
                            shape = RoundedCornerShape(16.dp),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = Terracotta,
                                focusedLabelColor = Terracotta,
                                focusedTextColor = textColor,
                                unfocusedTextColor = textColor
                            ),
                            modifier = Modifier.weight(1f)
                        )
                    }"""

content = content.replace(old_amount_field, new_amount_field)

# Use manualDate and manualTime when adding manual expense
old_add_manual = 'onAdd(Expense(manualTitle.ifBlank { "Spesa" }, manualCategory, parsedAmount, currentMonth))'
new_add_manual = 'onAdd(Expense(manualTitle.ifBlank { "Spesa" }, manualCategory, parsedAmount, currentMonth, date = manualDate, time = manualTime))'
content = content.replace(old_add_manual, new_add_manual)

# Also add current date and time to AI expense creation
old_add_ai = 'onAdd(Expense(parsedAi.title, parsedAi.category, amount, currentMonth))'
new_add_ai = """val currentDate = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())
                        val currentTime = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())
                        onAdd(Expense(parsedAi.title, parsedAi.category, amount, currentMonth, date = currentDate, time = currentTime))"""
content = content.replace(old_add_ai, new_add_ai)

# 3. Translate SetBudgetDialog subtitle and text field label
old_budget_text = """            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text(
                    "Imposta il tetto di spesa desiderato per ciascun mese. L'anello di progresso si aggiornerà automaticamente.",
                    color = textColor.copy(alpha = 0.8f),
                    fontSize = 13.sp
                )
                OutlinedTextField(
                    value = budgetText,
                    onValueChange = { budgetText = it },
                    label = { Text("Budget Mensile (€)") },"""

new_budget_text = """            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                val appLang = LocalAppLanguage.current
                Text(
                    AppStrings.get(AppStrings.imposta_il_tetto_di_spesa_desiderato_per_ciascun_mese_l_anello_di_progresso_si_aggiorner_automaticamente, appLang),
                    color = textColor.copy(alpha = 0.8f),
                    fontSize = 13.sp
                )
                OutlinedTextField(
                    value = budgetText,
                    onValueChange = { budgetText = it },
                    label = { Text(AppStrings.get(AppStrings.budget_mensile, appLang) + " (€)") },"""

content = content.replace(old_budget_text, new_budget_text)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Screenshot fixes applied successfully.")

