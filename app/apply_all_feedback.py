import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Fix SettingsScreen scrolling bug by adding .verticalScroll(rememberScrollState()) to its Column
settings_col_target = """        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {"""

settings_col_repl = """        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 20.dp)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {"""

content = content.replace(settings_col_target, settings_col_repl)

# 2. Fix AddReminderDialog dark mode colors and add quick date chips
add_reminder_dialog_old = """@Composable
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
    val appLang = LocalAppLanguage.current"""

add_reminder_dialog_new = """@Composable
fun AddReminderDialog(
    isDarkTheme: Boolean,
    onDismiss: () -> Unit,
    onAdd: (PaymentReminder) -> Unit
) {
    var title by remember { mutableStateOf("") }
    var amountStr by remember { mutableStateOf("") }
    
    val defaultDate = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())
    var dueDate by remember { mutableStateOf(defaultDate) }
    var isRecurring by remember { mutableStateOf(false) }
    var maxPaymentsStr by remember { mutableStateOf("") }

    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val dialogBg = if (isDarkTheme) Color(0xFF1D1B18) else Color.White
    val fieldBg = if (isDarkTheme) Color(0xFF2A2724) else Color.White
    val appLang = LocalAppLanguage.current"""

content = content.replace(add_reminder_dialog_old, add_reminder_dialog_new)

# Update OutlinedTextFields in AddReminderDialog to use proper dark theme colors and add quick date chips
reminder_text_fields_old = """                OutlinedTextField(
                    value = dueDate,
                    onValueChange = { dueDate = it },
                    label = { Text("Data scadenza (es. 25/10/2023)") },
                    singleLine = true,
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.fillMaxWidth()
                )"""

reminder_text_fields_new = """                OutlinedTextField(
                    value = dueDate,
                    onValueChange = { dueDate = it },
                    label = { Text("Data scadenza") },
                    singleLine = true,
                    shape = RoundedCornerShape(16.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Terracotta,
                        unfocusedBorderColor = Color.Gray,
                        focusedLabelColor = Terracotta,
                        focusedTextColor = textColor,
                        unfocusedTextColor = textColor,
                        focusedContainerColor = fieldBg,
                        unfocusedContainerColor = fieldBg
                    ),
                    modifier = Modifier.fillMaxWidth()
                )

                // Quick Date Chips
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    val cal = java.util.Calendar.getInstance()
                    val fmt = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault())
                    
                    Surface(
                        color = Terracotta.copy(alpha = 0.15f),
                        shape = CircleShape,
                        modifier = Modifier.clip(CircleShape).clickable { dueDate = fmt.format(cal.time) }
                    ) {
                        Text("Oggi", color = Terracotta, fontSize = 11.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp))
                    }
                    cal.add(java.util.Calendar.DAY_OF_YEAR, 7)
                    Surface(
                        color = Terracotta.copy(alpha = 0.15f),
                        shape = CircleShape,
                        modifier = Modifier.clip(CircleShape).clickable { dueDate = fmt.format(cal.time) }
                    ) {
                        Text("Tra 7 giorni", color = Terracotta, fontSize = 11.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp))
                    }
                    cal.add(java.util.Calendar.DAY_OF_YEAR, 23)
                    Surface(
                        color = Terracotta.copy(alpha = 0.15f),
                        shape = CircleShape,
                        modifier = Modifier.clip(CircleShape).clickable { dueDate = fmt.format(cal.time) }
                    ) {
                        Text("Tra 30 giorni", color = Terracotta, fontSize = 11.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp))
                    }
                }"""

content = content.replace(reminder_text_fields_old, reminder_text_fields_new)

# Also update title and amount OutlinedTextFields in AddReminderDialog to have proper dark colors
content = content.replace(
    """                OutlinedTextField(
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
                )""",
    """                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text(AppStrings.get(AppStrings.descrizione, appLang)) },
                    singleLine = true,
                    shape = RoundedCornerShape(16.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Terracotta,
                        unfocusedBorderColor = Color.Gray,
                        focusedLabelColor = Terracotta,
                        focusedTextColor = textColor,
                        unfocusedTextColor = textColor,
                        focusedContainerColor = fieldBg,
                        unfocusedContainerColor = fieldBg
                    ),
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = amountStr,
                    onValueChange = { amountStr = it },
                    label = { Text(AppStrings.get(AppStrings.importo, appLang)) },
                    singleLine = true,
                    shape = RoundedCornerShape(16.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Terracotta,
                        unfocusedBorderColor = Color.Gray,
                        focusedLabelColor = Terracotta,
                        focusedTextColor = textColor,
                        unfocusedTextColor = textColor,
                        focusedContainerColor = fieldBg,
                        unfocusedContainerColor = fieldBg
                    ),
                    modifier = Modifier.fillMaxWidth()
                )"""
)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Feedback applied successfully.")
