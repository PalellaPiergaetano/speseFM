import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add states in AddExpenseDialog
content = content.replace(
"""    var manualDate by remember { mutableStateOf(getCurrentDateString()) }""",
"""    var manualDate by remember { mutableStateOf(getCurrentDateString()) }
    var manualTime by remember { mutableStateOf("") }
    var manualDescription by remember { mutableStateOf("") }""")

# Add UI fields in AddExpenseDialog
content = content.replace(
"""                    OutlinedTextField(
                        value = manualDate,
                        onValueChange = { manualDate = it },
                        label = { Text(AppStrings.get(AppStrings.data_gg_mm_aaaa, LocalAppLanguage.current)) },""",
"""                    OutlinedTextField(
                        value = manualDate,
                        onValueChange = { manualDate = it },
                        label = { Text(AppStrings.get(AppStrings.data_gg_mm_aaaa, LocalAppLanguage.current)) },
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
                        value = manualTime,
                        onValueChange = { manualTime = it },
                        label = { Text("Ora (es. 14:30)") },
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
                        value = manualDescription,
                        onValueChange = { manualDescription = it },
                        label = { Text("Note aggiuntive (opzionale)") },""")

# Update onAdd call for Manual
content = content.replace(
"""                                    onAdd(
                                        Expense(
                                            title = manualTitle.trim(),
                                            category = manualCategory,
                                            amount = parsedAmt,
                                            month = monthToUse,
                                            date = dateToUse
                                        )
                                    )""",
"""                                    onAdd(
                                        Expense(
                                            title = manualTitle.trim(),
                                            category = manualCategory,
                                            amount = parsedAmt,
                                            month = monthToUse,
                                            date = dateToUse,
                                            time = manualTime.trim(),
                                            description = manualDescription.trim()
                                        )
                                    )""")

# Add ExpenseDetailDialog at the end of the file
dialog_code = """
@Composable
fun ExpenseDetailDialog(
    expense: Expense,
    isDarkTheme: Boolean,
    onDismiss: () -> Unit
) {
    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val dialogBg = if (isDarkTheme) Color(0xFF1D1B18) else Color.White
    val subTextColor = if (isDarkTheme) Color(0xFFA0B2A3) else Color(0xFF5B7B68)

    androidx.compose.material3.AlertDialog(
        onDismissRequest = onDismiss,
        shape = androidx.compose.foundation.shape.RoundedCornerShape(32.dp),
        containerColor = dialogBg,
        title = {
            androidx.compose.material3.Text("Dettaglio Uscita", color = textColor, fontWeight = FontWeight.Bold, fontSize = 20.sp)
        },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Titolo: ${expense.title}", color = textColor, fontSize = 16.sp)
                Text("Importo: ${formatAmount(expense.amount, false)}", color = textColor, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                Text("Categoria: ${expense.category}", color = textColor, fontSize = 16.sp)
                Text("Data: ${expense.date}", color = textColor, fontSize = 16.sp)
                if (expense.time.isNotBlank()) {
                    Text("Ora: ${expense.time}", color = textColor, fontSize = 16.sp)
                }
                if (expense.description.isNotBlank()) {
                    Text("Note: ${expense.description}", color = textColor, fontSize = 16.sp)
                }
            }
        },
        confirmButton = {
            androidx.compose.material3.TextButton(onClick = onDismiss) {
                Text("Chiudi", color = textColor)
            }
        }
    )
}
"""
content += dialog_code

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

