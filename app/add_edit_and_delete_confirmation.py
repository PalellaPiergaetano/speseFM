import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Add DeleteExpenseConfirmDialog and EditExpenseDialog at the end of the file
dialogs_code = """
@Composable
fun DeleteExpenseConfirmDialog(
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onConfirm: () -> Unit
) {
    val appLang = LocalAppLanguage.current
    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val dialogBg = if (isDarkTheme) Color(0xFF1D1B18) else Color.White

    AlertDialog(
        onDismissRequest = onDismiss,
        shape = RoundedCornerShape(28.dp),
        containerColor = dialogBg,
        title = {
            Text(AppStrings.get(AppStrings.conferma_eliminazione, appLang), color = textColor, fontWeight = FontWeight.Bold, fontSize = 20.sp)
        },
        text = {
            Text(AppStrings.get(AppStrings.sei_sicuro_di_voler_eliminare_questa_spesa, appLang), color = textColor.copy(alpha = 0.8f), fontSize = 14.sp)
        },
        confirmButton = {
            Button(
                onClick = {
                    onConfirm()
                    onDismiss()
                },
                shape = CircleShape,
                colors = ButtonDefaults.buttonColors(containerColor = Terracotta)
            ) {
                Text(AppStrings.get(AppStrings.elimina, appLang), color = Color.White, fontWeight = FontWeight.Bold)
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss, shape = CircleShape) {
                Text(AppStrings.get(AppStrings.annulla, appLang), color = Sage)
            }
        }
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EditExpenseDialog(
    expense: Expense,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onSave: (Expense) -> Unit
) {
    var title by remember { mutableStateOf(expense.title) }
    var amountStr by remember { mutableStateOf(expense.amount.toString()) }
    var category by remember { mutableStateOf(expense.category) }
    var date by remember { mutableStateOf(expense.date) }
    var time by remember { mutableStateOf(expense.time) }
    var description by remember { mutableStateOf(expense.description) }
    var dropdownExpanded by remember { mutableStateOf(false) }

    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val dialogBg = if (isDarkTheme) Color(0xFF1D1B18) else Color.White
    val appLang = LocalAppLanguage.current

    AlertDialog(
        onDismissRequest = onDismiss,
        shape = RoundedCornerShape(32.dp),
        containerColor = dialogBg,
        title = {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(
                    modifier = Modifier
                        .size(40.dp)
                        .background(Terracotta.copy(alpha = 0.15f), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.Edit, contentDescription = null, tint = Terracotta)
                }
                Spacer(Modifier.width(12.dp))
                Text(AppStrings.get(AppStrings.modifica_spesa, appLang), color = textColor, fontWeight = FontWeight.Bold, fontSize = 20.sp)
            }
        },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text(AppStrings.get(AppStrings.descrizione, appLang)) },
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

                OutlinedTextField(
                    value = amountStr,
                    onValueChange = { amountStr = it },
                    label = { Text(AppStrings.get(AppStrings.importo, appLang) + " (€)") },
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
                        value = date,
                        onValueChange = { date = it },
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
                        value = time,
                        onValueChange = { time = it },
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
                }

                Text(AppStrings.get(AppStrings.categoria, appLang), color = textColor, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)

                ExposedDropdownMenuBox(
                    expanded = dropdownExpanded,
                    onExpandedChange = { dropdownExpanded = !dropdownExpanded },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    val currentMeta = getCategoryMeta(category)
                    OutlinedTextField(
                        value = AppStrings.translateCategory(category, appLang),
                        onValueChange = {},
                        readOnly = true,
                        label = { Text(AppStrings.get(AppStrings.seleziona_categoria, appLang)) },
                        leadingIcon = {
                            Box(
                                modifier = Modifier
                                    .size(28.dp)
                                    .background(currentMeta.color.copy(alpha = 0.15f), CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = currentMeta.icon,
                                    contentDescription = null,
                                    tint = currentMeta.color,
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = dropdownExpanded) },
                        shape = RoundedCornerShape(16.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Terracotta,
                            focusedLabelColor = Terracotta,
                            focusedTextColor = textColor,
                            unfocusedTextColor = textColor
                        ),
                        modifier = Modifier
                            .menuAnchor(MenuAnchorType.PrimaryNotEditable, true)
                            .fillMaxWidth()
                    )

                    ExposedDropdownMenu(
                        expanded = dropdownExpanded,
                        onDismissRequest = { dropdownExpanded = false },
                        modifier = Modifier.background(dialogBg)
                    ) {
                        allCategories.forEach { cat ->
                            val meta = getCategoryMeta(cat)
                            DropdownMenuItem(
                                text = {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Box(
                                            modifier = Modifier
                                                .size(28.dp)
                                                .background(meta.color.copy(alpha = 0.15f), CircleShape),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Icon(
                                                imageVector = meta.icon,
                                                contentDescription = null,
                                                tint = meta.color,
                                                modifier = Modifier.size(16.dp)
                                            )
                                        }
                                        Spacer(Modifier.width(12.dp))
                                        Text(
                                            AppStrings.translateCategory(cat, appLang),
                                            color = textColor,
                                            fontWeight = if (cat == category) FontWeight.Bold else FontWeight.Normal
                                        )
                                    }
                                },
                                onClick = {
                                    category = cat
                                    dropdownExpanded = false
                                }
                            )
                        }
                    }
                }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val parsedAmount = parseAmount(amountStr) ?: expense.amount
                    val derivedMonth = getExpenseMonthFromDate(date)
                    val updated = expense.copy(
                        title = title.ifBlank { "Spesa" },
                        amount = parsedAmount,
                        category = category,
                        month = derivedMonth,
                        date = date,
                        time = time,
                        description = description
                    )
                    onSave(updated)
                    onDismiss()
                },
                shape = CircleShape,
                colors = ButtonDefaults.buttonColors(containerColor = Terracotta)
            ) {
                Text(AppStrings.get(AppStrings.salva, appLang), color = Color.White, fontWeight = FontWeight.Bold)
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss, shape = CircleShape) {
                Text(AppStrings.get(AppStrings.annulla, appLang), color = Sage)
            }
        }
    )
}
"""

if "fun EditExpenseDialog" not in content:
    content = content + "\n" + dialogs_code

# 2. Update ExpenseDetailScreen to include Edit button in TopAppBar and Delete confirmation
old_detail_screen = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ExpenseDetailScreen(
    expense: Expense,
    isDark: Boolean,
    onClose: () -> Unit,
    onDelete: () -> Unit
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    val appLang = LocalAppLanguage.current

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(AppStrings.get(AppStrings.dettagli_spesa, appLang), color = textColor, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    androidx.compose.material3.IconButton(onClick = onClose) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = AppStrings.get(AppStrings.indietro, appLang), tint = textColor)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },
        containerColor = if (isDark) Color(0xFF121110) else Color(0xFFFAF7F2)
    ) { padding ->"""

new_detail_screen = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ExpenseDetailScreen(
    expense: Expense,
    isDark: Boolean,
    onClose: () -> Unit,
    onDelete: () -> Unit,
    onSaveEdit: (Expense) -> Unit
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    val appLang = LocalAppLanguage.current

    var showEditDialog by remember { mutableStateOf(false) }
    var showDeleteConfirm by remember { mutableStateOf(false) }

    if (showEditDialog) {
        EditExpenseDialog(
            expense = expense,
            isDarkTheme = isDark,
            onDismiss = { showEditDialog = false },
            onSave = { updated ->
                onSaveEdit(updated)
            }
        )
    }

    if (showDeleteConfirm) {
        DeleteExpenseConfirmDialog(
            isDarkTheme = isDark,
            onDismiss = { showDeleteConfirm = false },
            onConfirm = {
                onDelete()
                onClose()
            }
        )
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(AppStrings.get(AppStrings.dettagli_spesa, appLang), color = textColor, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    androidx.compose.material3.IconButton(onClick = onClose) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = AppStrings.get(AppStrings.indietro, appLang), tint = textColor)
                    }
                },
                actions = {
                    androidx.compose.material3.IconButton(onClick = { showEditDialog = true }) {
                        Icon(Icons.Default.Edit, contentDescription = AppStrings.get(AppStrings.modifica, appLang), tint = textColor)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },
        containerColor = if (isDark) Color(0xFF121110) else Color(0xFFFAF7F2)
    ) { padding ->"""

content = content.replace(old_detail_screen, new_detail_screen)

# Update delete button in ExpenseDetailScreen to trigger showDeleteConfirm
content = content.replace("onClick = { onDelete(); onClose() },", "onClick = { showDeleteConfirm = true },")

# 3. Update ExpenseDetailScreen call inside SpeseApp
old_expense_detail_call = """                if (selectedExpense != null) {
                    BackHandler { selectedExpense = null }
                    ExpenseDetailScreen(
                        expense = selectedExpense!!,
                        isDark = isDarkTheme,
                        onClose = { selectedExpense = null },
                        onDelete = { 
                            val e = selectedExpense!!
                            expenses = expenses.filter { it != e }
                            saveExpenses(context, expenses)
                            selectedExpense = null
                        }
                    )
                }"""

new_expense_detail_call = """                if (selectedExpense != null) {
                    BackHandler { selectedExpense = null }
                    ExpenseDetailScreen(
                        expense = selectedExpense!!,
                        isDark = isDarkTheme,
                        onClose = { selectedExpense = null },
                        onDelete = { 
                            val e = selectedExpense!!
                            expenses = expenses.filter { it != e }
                            saveExpenses(context, expenses)
                            selectedExpense = null
                        },
                        onSaveEdit = { updated ->
                            expenses = expenses.map { if (it == selectedExpense) updated else it }
                            saveExpenses(context, expenses)
                            selectedExpense = updated
                        }
                    )
                }"""

content = content.replace(old_expense_detail_call, new_expense_detail_call)

# 4. Update ExpenseRow delete icon to ask for confirmation before deleting
old_row_delete_button = """IconButton(onClick = { onDelete(expense) }) {"""
new_row_delete_button = """
            var showRowDeleteConfirm by remember { mutableStateOf(false) }
            if (showRowDeleteConfirm) {
                DeleteExpenseConfirmDialog(
                    isDarkTheme = isDark,
                    onDismiss = { showRowDeleteConfirm = false },
                    onConfirm = { onDelete(expense) }
                )
            }
            IconButton(onClick = { showRowDeleteConfirm = true }) {"""

content = content.replace(old_row_delete_button, new_row_delete_button)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Edit expense and delete confirmation implemented successfully.")

