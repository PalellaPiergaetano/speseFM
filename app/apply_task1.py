with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
"""data class PaymentReminder(
    val id: String = UUID.randomUUID().toString(),
    val title: String,
    val amount: Double,
    val dueDate: String,
    val category: String = "Altro",
    val isCompleted: Boolean = false,
    val recurrence: ReminderRecurrence = ReminderRecurrence.NONE
)""",
"""data class PaymentReminder(
    val id: String = UUID.randomUUID().toString(),
    val title: String,
    val amount: Double,
    val dueDate: String,
    val category: String = "Altro",
    val isCompleted: Boolean = false,
    val recurrence: ReminderRecurrence = ReminderRecurrence.NONE,
    val maxPayments: Int = 1,
    val paymentsMade: Int = 0
)""")

content = content.replace(
"""        if (parts.size >= 4) {
            PaymentReminder(
                id = parts[0],
                title = parts[1],
                amount = parseAmount(parts[2]) ?: 0.0,
                dueDate = parts[3],
                category = if (parts.size >= 5) parts[4] else "Altro",
                isCompleted = if (parts.size >= 6) parts[5].toBoolean() else false,
                recurrence = if (parts.size >= 7) {
                    try { ReminderRecurrence.valueOf(parts[6]) } catch (e: Exception) { ReminderRecurrence.NONE }
                } else ReminderRecurrence.NONE
            )
        } else null""",
"""        if (parts.size >= 4) {
            PaymentReminder(
                id = parts[0],
                title = parts[1],
                amount = parseAmount(parts[2]) ?: 0.0,
                dueDate = parts[3],
                category = if (parts.size >= 5) parts[4] else "Altro",
                isCompleted = if (parts.size >= 6) parts[5].toBoolean() else false,
                recurrence = if (parts.size >= 7) {
                    try { ReminderRecurrence.valueOf(parts[6]) } catch (e: Exception) { ReminderRecurrence.NONE }
                } else ReminderRecurrence.NONE,
                maxPayments = if (parts.size >= 8) parts[7].toIntOrNull() ?: 1 else 1,
                paymentsMade = if (parts.size >= 9) parts[8].toIntOrNull() ?: 0 else 0
            )
        } else null""")

content = content.replace(
"""private fun saveReminders(context: Context, reminders: List<PaymentReminder>) {
    val raw = reminders.joinToString("\\n") {
        "${it.id}\\t${it.title}\\t${it.amount}\\t${it.dueDate}\\t${it.category}\\t${it.isCompleted}\\t${it.recurrence.name}"
    }""",
"""private fun saveReminders(context: Context, reminders: List<PaymentReminder>) {
    val raw = reminders.joinToString("\\n") {
        "${it.id}\\t${it.title}\\t${it.amount}\\t${it.dueDate}\\t${it.category}\\t${it.isCompleted}\\t${it.recurrence.name}\\t${it.maxPayments}\\t${it.paymentsMade}"
    }""")

content = content.replace(
"""            onPayReminder = { rem ->
                val dateToUse = rem.dueDate.ifBlank { getCurrentDateString() }
                val monthToUse = deriveMonthFromDate(dateToUse)
                val newExp = Expense(
                    title = rem.title,
                    category = rem.category,
                    amount = rem.amount,
                    month = monthToUse,
                    date = dateToUse
                )
                expenses = listOf(newExp) + expenses
                saveExpenses(context, expenses)

                reminders = if (rem.recurrence == ReminderRecurrence.NONE) {
                    reminders.map { if (it.id == rem.id) it.copy(isCompleted = true) else it }
                } else {
                    val nextDueDate = advanceDueDate(rem.dueDate, rem.recurrence)
                    reminders.map { if (it.id == rem.id) it.copy(dueDate = nextDueDate, isCompleted = false) else it }
                }
                saveReminders(context, reminders)

                val msg = if (rem.recurrence == ReminderRecurrence.NONE) {
                    "Pagamento registrato come spesa!"
                } else {
                    val nextDueDate = advanceDueDate(rem.dueDate, rem.recurrence)
                    "Spesa registrata! Promemoria aggiornato al $nextDueDate"
                }
                Toast.makeText(context, msg, Toast.LENGTH_LONG).show()
            },""",
"""            onPayReminder = { rem ->
                val dateToUse = rem.dueDate.ifBlank { getCurrentDateString() }
                val monthToUse = deriveMonthFromDate(dateToUse)
                val newExp = Expense(
                    title = rem.title,
                    category = rem.category,
                    amount = rem.amount,
                    month = monthToUse,
                    date = dateToUse
                )
                expenses = listOf(newExp) + expenses
                saveExpenses(context, expenses)

                val updatedPaymentsMade = rem.paymentsMade + 1
                val isFullyPaid = updatedPaymentsMade >= rem.maxPayments

                reminders = if (isFullyPaid) {
                    if (rem.recurrence == ReminderRecurrence.NONE) {
                        reminders.map { if (it.id == rem.id) it.copy(isCompleted = true, paymentsMade = updatedPaymentsMade) else it }
                    } else {
                        val nextDueDate = advanceDueDate(rem.dueDate, rem.recurrence)
                        reminders.map { if (it.id == rem.id) it.copy(dueDate = nextDueDate, isCompleted = false, paymentsMade = 0) else it }
                    }
                } else {
                    reminders.map { if (it.id == rem.id) it.copy(paymentsMade = updatedPaymentsMade) else it }
                }
                saveReminders(context, reminders)

                val msg = if (isFullyPaid) {
                    if (rem.recurrence == ReminderRecurrence.NONE) {
                        "Pagamento completato e registrato come spesa!"
                    } else {
                        val nextDueDate = advanceDueDate(rem.dueDate, rem.recurrence)
                        "Spesa registrata! Promemoria aggiornato al $nextDueDate"
                    }
                } else {
                    "Pagamento $updatedPaymentsMade di ${rem.maxPayments} registrato!"
                }
                Toast.makeText(context, msg, Toast.LENGTH_LONG).show()
            },""")

content = content.replace(
"""    var showAddForm by remember { mutableStateOf(false) }
    var title by remember { mutableStateOf("") }
    var amount by remember { mutableStateOf("") }
    var dueDate by remember { mutableStateOf(getCurrentDateString()) }
    var category by remember { mutableStateOf(allCategories[0]) }
    var recurrence by remember { mutableStateOf(ReminderRecurrence.NONE) }""",
"""    var showAddForm by remember { mutableStateOf(false) }
    var title by remember { mutableStateOf("") }
    var amount by remember { mutableStateOf("") }
    var dueDate by remember { mutableStateOf(getCurrentDateString()) }
    var maxPayments by remember { mutableStateOf("1") }
    var category by remember { mutableStateOf(allCategories[0]) }
    var recurrence by remember { mutableStateOf(ReminderRecurrence.NONE) }""")

content = content.replace(
"""                                    val recurrenceText = if (reminder.recurrence != ReminderRecurrence.NONE) " • 🔄 ${reminder.recurrence.displayNameIt}" else ""
                                    Text(
                                        "Scadenza: ${reminder.dueDate}$recurrenceText • ${formatAmount(reminder.amount, false)}",
                                        color = if (reminder.isCompleted) subTextColor else Rose,
                                        fontSize = 11.sp,""",
"""                                    val recurrenceText = if (reminder.recurrence != ReminderRecurrence.NONE) " • 🔄 ${reminder.recurrence.displayNameIt}" else ""
                                    val paymentsProgress = if (reminder.maxPayments > 1) " • Pagati: ${reminder.paymentsMade}/${reminder.maxPayments}" else ""
                                    Text(
                                        "Scadenza: ${reminder.dueDate}$recurrenceText$paymentsProgress • ${formatAmount(reminder.amount, false)}",
                                        color = if (reminder.isCompleted) subTextColor else Rose,
                                        fontSize = 11.sp,""")

content = content.replace(
"""                    OutlinedTextField(
                        value = dueDate,
                        onValueChange = { dueDate = it },
                        label = { Text("Data Scadenza (gg/mm/aaaa)") },
                        singleLine = true,
                        shape = RoundedCornerShape(16.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Rose,
                            focusedLabelColor = Rose,
                            focusedTextColor = textColor,
                            unfocusedTextColor = textColor
                        ),
                        modifier = Modifier.fillMaxWidth()
                    )

                    Text("Ricorrenza", color = textColor, fontSize = 13.sp, fontWeight = FontWeight.Bold)""",
"""                    OutlinedTextField(
                        value = dueDate,
                        onValueChange = { dueDate = it },
                        label = { Text("Data Scadenza (gg/mm/aaaa)") },
                        singleLine = true,
                        shape = RoundedCornerShape(16.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Rose,
                            focusedLabelColor = Rose,
                            focusedTextColor = textColor,
                            unfocusedTextColor = textColor
                        ),
                        modifier = Modifier.fillMaxWidth()
                    )

                    OutlinedTextField(
                        value = maxPayments,
                        onValueChange = { maxPayments = it.filter { char -> char.isDigit() } },
                        label = { Text("Numero max pagamenti/mese") },
                        singleLine = true,
                        keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(keyboardType = androidx.compose.ui.text.input.KeyboardType.Number),
                        shape = RoundedCornerShape(16.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Rose,
                            focusedLabelColor = Rose,
                            focusedTextColor = textColor,
                            unfocusedTextColor = textColor
                        ),
                        modifier = Modifier.fillMaxWidth()
                    )

                    Text("Ricorrenza", color = textColor, fontSize = 13.sp, fontWeight = FontWeight.Bold)""")

content = content.replace(
"""                                    onAddReminder(
                                        PaymentReminder(
                                            title = title.trim(),
                                            amount = parsedAmt,
                                            dueDate = dueDate.ifBlank { getCurrentDateString() },
                                            category = category,
                                            recurrence = recurrence
                                        )
                                    )
                                    showAddForm = false
                                    title = ""
                                    amount = ""
                                    recurrence = ReminderRecurrence.NONE""",
"""                                    onAddReminder(
                                        PaymentReminder(
                                            title = title.trim(),
                                            amount = parsedAmt,
                                            dueDate = dueDate.ifBlank { getCurrentDateString() },
                                            category = category,
                                            recurrence = recurrence,
                                            maxPayments = maxPayments.toIntOrNull()?.coerceAtLeast(1) ?: 1
                                        )
                                    )
                                    showAddForm = false
                                    title = ""
                                    amount = ""
                                    maxPayments = "1"
                                    recurrence = ReminderRecurrence.NONE""")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

