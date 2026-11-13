import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Add PaymentReminder data class and persistence
reminder_model_code = """
data class PaymentReminder(
    val title: String,
    val amount: Double,
    val dueDate: String,
    val isRecurring: Boolean = false,
    val recurrenceInterval: String? = null,
    val maxPayments: Int? = null,
    val paymentsMade: Int = 0
)

private fun loadPaymentReminders(context: Context): List<PaymentReminder> {
    val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
    val json = prefs.getString("payment_reminders", null) ?: return emptyList()
    val type = object : com.google.gson.reflect.TypeToken<List<PaymentReminder>>() {}.type
    return try {
        com.google.gson.Gson().fromJson(json, type) ?: emptyList()
    } catch (e: Exception) {
        emptyList()
    }
}

private fun savePaymentReminders(context: Context, reminders: List<PaymentReminder>) {
    val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
    val json = com.google.gson.Gson().toJson(reminders)
    prefs.edit().putString("payment_reminders", json).apply()
}
"""

if "data class PaymentReminder" not in content:
    content = content.replace("data class Expense(", reminder_model_code + "\n\ndata class Expense(")

# 2. Add Date and Time fields to AddExpenseDialog
manual_col_target = """                // INSERIMENTO MANUALE
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    OutlinedTextField(
                        value = manualTitle,
                        onValueChange = { manualTitle = it },
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
                        value = manualAmount,
                        onValueChange = { manualAmount = it },
                        label = { Text(AppStrings.get(AppStrings.importo, appLang)) },
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

manual_col_repl = """                // INSERIMENTO MANUALE
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    var manualDate by remember { mutableStateOf(java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())) }
                    var manualTime by remember { mutableStateOf(java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date())) }

                    OutlinedTextField(
                        value = manualTitle,
                        onValueChange = { manualTitle = it },
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
                        value = manualAmount,
                        onValueChange = { manualAmount = it },
                        label = { Text(AppStrings.get(AppStrings.importo, appLang)) },
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

content = content.replace(manual_col_target, manual_col_repl)

# Update manual add action to use manualDate and manualTime
old_manual_add = 'onAdd(Expense(manualTitle.ifBlank { "Spesa" }, manualCategory, parsedAmount, currentMonth, date = currentDate, time = currentTime))'
new_manual_add = 'onAdd(Expense(manualTitle.ifBlank { "Spesa" }, manualCategory, parsedAmount, currentMonth, date = manualDate, time = manualTime))'
content = content.replace(old_manual_add, new_manual_add)

# 3. Add Reminders Screen and Dialog at the end of the file
reminders_code = """
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RemindersScreen(
    reminders: List<PaymentReminder>,
    isDark: Boolean,
    onAddReminder: (PaymentReminder) -> Unit,
    onDeleteReminder: (PaymentReminder) -> Unit,
    onPayReminder: (PaymentReminder) -> Unit,
    modifier: Modifier
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    val appLang = LocalAppLanguage.current

    var showAddDialog by remember { mutableStateOf(false) }

    if (showAddDialog) {
        AddReminderDialog(
            isDarkTheme = isDark,
            onDismiss = { showAddDialog = false },
            onAdd = { 
                onAddReminder(it)
                showAddDialog = false
            }
        )
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(AppStrings.get(AppStrings.promemoria_pagamenti, appLang), color = textColor, fontWeight = FontWeight.Bold, fontSize = 28.sp) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { showAddDialog = true },
                shape = CircleShape,
                containerColor = Terracotta,
                contentColor = Color.White
            ) {
                Icon(Icons.Default.Add, contentDescription = null)
            }
        },
        containerColor = Color.Transparent
    ) { padding ->
        if (reminders.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.NotificationsNone, contentDescription = null, tint = subTextColor, modifier = Modifier.size(64.dp))
                    Spacer(Modifier.height(16.dp))
                    Text(
                        AppStrings.get(AppStrings.nessun_promemoria_attivo_aggiungine_uno_per_non_dimenticare_le_tue_scadenze, appLang),
                        color = subTextColor,
                        fontSize = 14.sp,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(horizontal = 32.dp)
                    )
                }
            }
        } else {
            LazyColumn(
                modifier = modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(horizontal = 20.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                item { Spacer(Modifier.height(8.dp)) }
                items(reminders) { reminder ->
                    ReminderCard(reminder, isDark, onPay = { onPayReminder(reminder) }, onDelete = { onDeleteReminder(reminder) })
                }
                item { Spacer(Modifier.height(80.dp)) }
            }
        }
    }
}

@Composable
fun ReminderCard(
    reminder: PaymentReminder,
    isDark: Boolean,
    onPay: () -> Unit,
    onDelete: () -> Unit
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val cardBg = if (isDark) Color(0xFF2A2724) else Color.White
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    val appLang = LocalAppLanguage.current

    Surface(
        color = cardBg,
        shape = RoundedCornerShape(20.dp),
        shadowElevation = 2.dp,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .background(Terracotta.copy(alpha = 0.15f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.Notifications, contentDescription = null, tint = Terracotta)
            }
            Spacer(Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(reminder.title, color = textColor, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(4.dp))
                Text("Scadenza: ${reminder.dueDate}", color = subTextColor, fontSize = 12.sp)
                if (reminder.maxPayments != null) {
                    Text("Rate: ${reminder.paymentsMade}/${reminder.maxPayments}", color = subTextColor, fontSize = 11.sp)
                }
            }
            Column(horizontalAlignment = Alignment.End) {
                Text(
                    text = "${String.format(Locale.getDefault(), "%.2f", reminder.amount)} €",
                    color = Terracotta,
                    fontWeight = FontWeight.ExtraBold,
                    fontSize = 16.sp
                )
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    TextButton(onClick = onDelete, contentPadding = PaddingValues(4.dp)) {
                        Text(AppStrings.get(AppStrings.elimina, appLang), color = Color.Gray, fontSize = 12.sp)
                    }
                    Button(
                        onClick = onPay,
                        shape = CircleShape,
                        colors = ButtonDefaults.buttonColors(containerColor = Sage),
                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                        modifier = Modifier.height(32.dp)
                    ) {
                        Text(AppStrings.get(AppStrings.paga_ora, appLang), color = Color.White, fontSize = 12.sp)
                    }
                }
            }
        }
    }
}

@Composable
fun AddReminderDialog(
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (PaymentReminder) -> Unit
) {
    var title by remember { mutableStateOf("") }
    var amountStr by remember { mutableStateOf("") }
    var dueDate by remember { mutableStateOf("") }
    var isRecurring by remember { mutableStateOf(false) }
    var maxPaymentsStr by remember { mutableStateOf("") }

    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val dialogBg = if (isDarkTheme) Color(0xFF1D1B18) else Color.White
    val appLang = LocalAppLanguage.current

    AlertDialog(
        onDismissRequest = onDismiss,
        shape = RoundedCornerShape(32.dp),
        containerColor = dialogBg,
        title = {
            Text(AppStrings.get(AppStrings.nuovo_promemoria, appLang), color = textColor, fontWeight = FontWeight.Bold, fontSize = 20.sp)
        },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text(AppStrings.get(AppStrings.descrizione, appLang)) },
                    singleLine = true,
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = amountStr,
                    onValueChange = { amountStr = it },
                    label = { Text(AppStrings.get(AppStrings.importo, appLang)) },
                    singleLine = true,
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = dueDate,
                    onValueChange = { dueDate = it },
                    label = { Text("Data scadenza (es. 25/10/2023)") },
                    singleLine = true,
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.fillMaxWidth()
                )
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = isRecurring, onCheckedChange = { isRecurring = it })
                    Spacer(Modifier.width(8.dp))
                    Text(AppStrings.get(AppStrings.ricorrenza, appLang), color = textColor)
                }
                if (isRecurring) {
                    OutlinedTextField(
                        value = maxPaymentsStr,
                        onValueChange = { maxPaymentsStr = it },
                        label = { Text(AppStrings.get(AppStrings.numero_max_pagamenti_mese, appLang)) },
                        singleLine = true,
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val amount = parseAmount(amountStr) ?: 0.0
                    if (title.isNotBlank() && amount > 0) {
                        val maxP = maxPaymentsStr.toIntOrNull()
                        onAdd(PaymentReminder(title, amount, dueDate.ifBlank { "Prossimamente" }, isRecurring, if (isRecurring) "Mensile" else null, maxP, 0))
                    }
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

if "fun RemindersScreen" not in content:
    content = content + "\n" + reminders_code

# 4. Add reminders state and 4th tab in SpeseApp
spese_app_reminders_state = """    var reminders by remember { mutableStateOf(loadPaymentReminders(context)) }"""
if "var reminders" not in content:
    content = content.replace("var expenses by remember { mutableStateOf(loadExpenses(context)) }", "var expenses by remember { mutableStateOf(loadExpenses(context)) }\n    " + spese_app_reminders_state)

# Add 4th tab in BottomBar
old_bottom_bar = """                                val appLang = LocalAppLanguage.current
                                listOf(
                                    AppStrings.get(AppStrings.panoramica_spese, appLang) to Icons.Default.Home,
                                    AppStrings.get(AppStrings.movimenti, appLang) to Icons.AutoMirrored.Filled.ReceiptLong,
                                    AppStrings.get(AppStrings.report_statistiche, appLang) to Icons.Default.BarChart
                                ).forEachIndexed { index, item ->"""

new_bottom_bar = """                                val appLang = LocalAppLanguage.current
                                listOf(
                                    AppStrings.get(AppStrings.panoramica_spese, appLang) to Icons.Default.Home,
                                    AppStrings.get(AppStrings.movimenti, appLang) to Icons.AutoMirrored.Filled.ReceiptLong,
                                    AppStrings.get(AppStrings.report_statistiche, appLang) to Icons.Default.BarChart,
                                    AppStrings.get(AppStrings.promemoria, appLang) to Icons.Default.Notifications
                                ).forEachIndexed { index, item ->"""
content = content.replace(old_bottom_bar, new_bottom_bar)

# Add case `3 -> RemindersScreen(...)` in when(selectedTab)
when_target = """                        2 -> Reports(
                            allExpenses = expenses,
                            filteredExpenses = activeMonthExpenses,
                            total = total,
                            numMonths = activeNumMonths,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,
                            onMonthSelect = { selectedMonthFilter = it },
                            modifier = Modifier.padding(padding)
                        )"""

when_repl = """                        2 -> Reports(
                            allExpenses = expenses,
                            filteredExpenses = activeMonthExpenses,
                            total = total,
                            numMonths = activeNumMonths,
                            availableMonths = availableMonths,
                            selectedMonth = selectedMonthFilter,
                            isDark = isDarkTheme,
                            isPrivacyMode = isPrivacyMode,
                            onMonthSelect = { selectedMonthFilter = it },
                            modifier = Modifier.padding(padding)
                        )
                        3 -> RemindersScreen(
                            reminders = reminders,
                            isDark = isDarkTheme,
                            onAddReminder = { 
                                reminders = reminders + it
                                savePaymentReminders(context, reminders)
                                Toast.makeText(context, AppStrings.get(AppStrings.promemoria_salvato, appLang), Toast.LENGTH_SHORT).show()
                            },
                            onDeleteReminder = { 
                                reminders = reminders.filter { r -> r != it }
                                savePaymentReminders(context, reminders)
                            },
                            onPayReminder = { reminder ->
                                val newExp = Expense(title = reminder.title, category = "Fitto / Bollette / Casa", amount = reminder.amount, month = currentMonth, date = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date()), time = java.text.SimpleDateFormat("HH:mm", java.util.Locale.getDefault()).format(java.util.Date()))
                                expenses = expenses + newExp
                                saveExpenses(context, expenses)
                                
                                reminders = reminders.map { r ->
                                    if (r == reminder) {
                                        r.copy(paymentsMade = r.paymentsMade + 1)
                                    } else r
                                }
                                savePaymentReminders(context, reminders)
                                Toast.makeText(context, "Pagamento registrato!", Toast.LENGTH_SHORT).show()
                            },
                            modifier = Modifier.padding(padding)
                        )"""

content = content.replace(when_target, when_repl)

# Add necessary icon import for Notifications and NotificationsNone
imports_add = """
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.NotificationsNone
import androidx.compose.material3.Checkbox
"""
if "import androidx.compose.material.icons.filled.Notifications" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Add", imports_add.strip() + "\nimport androidx.compose.material.icons.filled.Add")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

