import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

screens_code = """
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onTogglePrivacy: () -> Unit,
    onLockClick: () -> Unit,
    onImportClick: () -> Unit,
    onExportClick: () -> Unit,
    onClearAllClick: () -> Unit,
    onOpenTutorialClick: () -> Unit,
    onLanguageClick: () -> Unit,
    onRemindersClick: () -> Unit,
    onClose: () -> Unit
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val appLang = LocalAppLanguage.current
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
    val paperColor = if (isDark) Color(0xFF121110) else Color(0xFFFAF7F2)

    Box(modifier = Modifier.fillMaxSize().background(paperColor)) {
        BackgroundCircles(isDark)

        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text(AppStrings.get(AppStrings.impostazioni, appLang), color = textColor, fontWeight = FontWeight.Bold) },
                    navigationIcon = {
                        androidx.compose.material3.IconButton(onClick = onClose) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = AppStrings.get(AppStrings.indietro, appLang), tint = textColor)
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
                )
            },
            containerColor = Color.Transparent
        ) { padding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(horizontal = 20.dp)
                    .verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Spacer(Modifier.height(8.dp))
                
                SettingsItemRow(
                    icon = Icons.Default.Language,
                    title = AppStrings.get(AppStrings.lingua, appLang),
                    subtitle = appLang.displayName,
                    onClick = onLanguageClick,
                    isDark = isDark,
                    cardBg = cardBg,
                    textColor = textColor
                )

                SettingsItemRow(
                    icon = Icons.Default.Notifications,
                    title = AppStrings.get(AppStrings.promemoria_pagamenti, appLang),
                    subtitle = AppStrings.get(AppStrings.scadenze, appLang),
                    onClick = onRemindersClick,
                    isDark = isDark,
                    cardBg = cardBg,
                    textColor = textColor
                )

                SettingsItemRow(
                    icon = if (isPrivacyMode) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                    title = AppStrings.get(AppStrings.privacy, appLang),
                    subtitle = AppStrings.get(AppStrings.nascondi_saldi, appLang),
                    onClick = onTogglePrivacy,
                    isDark = isDark,
                    cardBg = cardBg,
                    textColor = textColor,
                    action = {
                        androidx.compose.material3.Switch(checked = isPrivacyMode, onCheckedChange = { onTogglePrivacy() })
                    }
                )

                SettingsItemRow(
                    icon = Icons.Default.Lock,
                    title = AppStrings.get(AppStrings.sicurezza, appLang),
                    subtitle = AppStrings.get(AppStrings.blocca_ora, appLang),
                    onClick = onLockClick,
                    isDark = isDark,
                    cardBg = cardBg,
                    textColor = textColor
                )
                
                SettingsItemRow(
                    icon = Icons.Default.FileDownload,
                    title = AppStrings.get(AppStrings.importa, appLang),
                    subtitle = AppStrings.get(AppStrings.xls_csv, appLang),
                    onClick = onImportClick,
                    isDark = isDark,
                    cardBg = cardBg,
                    textColor = textColor
                )
                
                SettingsItemRow(
                    icon = Icons.Default.FileUpload,
                    title = AppStrings.get(AppStrings.esporta, appLang),
                    subtitle = AppStrings.get(AppStrings.backup_csv, appLang),
                    onClick = onExportClick,
                    isDark = isDark,
                    cardBg = cardBg,
                    textColor = textColor
                )

                SettingsItemRow(
                    icon = Icons.Default.HelpOutline,
                    title = AppStrings.get(AppStrings.guida, appLang),
                    subtitle = AppStrings.get(AppStrings.tutorial_app, appLang),
                    onClick = onOpenTutorialClick,
                    isDark = isDark,
                    cardBg = cardBg,
                    textColor = textColor
                )
                
                SettingsItemRow(
                    icon = Icons.Default.DeleteForever,
                    title = AppStrings.get(AppStrings.svuota, appLang),
                    subtitle = AppStrings.get(AppStrings.reset_dati, appLang),
                    onClick = onClearAllClick,
                    isDark = isDark,
                    cardBg = cardBg,
                    textColor = Color(0xFFD95D39)
                )
            }
        }
    }
}

@Composable
fun SettingsItemRow(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    title: String,
    subtitle: String,
    onClick: () -> Unit,
    isDark: Boolean,
    cardBg: Color,
    textColor: Color,
    action: @Composable (() -> Unit)? = null
) {
    val subTextColor = if (isDark) Color(0xFFA0B2A3) else Color(0xFF5B7B68)
    Surface(
        onClick = onClick,
        color = cardBg,
        shape = RoundedCornerShape(16.dp),
        shadowElevation = 2.dp,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .background(Terracotta.copy(alpha = 0.15f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(icon, contentDescription = title, tint = Terracotta)
            }
            Spacer(Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(title, color = textColor, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                Text(subtitle, color = subTextColor, fontSize = 12.sp)
            }
            if (action != null) {
                action()
            } else {
                Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = subTextColor)
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
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
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Spacer(Modifier.height(16.dp))
            
            Surface(
                color = cardBg,
                shape = RoundedCornerShape(16.dp),
                shadowElevation = 4.dp,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                    val catInfo = getCategoryMeta(expense.category)
                    Box(
                        modifier = Modifier
                            .size(64.dp)
                            .background(catInfo.color.copy(alpha = 0.2f), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(catInfo.icon, contentDescription = null, tint = catInfo.color, modifier = Modifier.size(32.dp))
                    }
                    Spacer(Modifier.height(16.dp))
                    Text(expense.title, color = textColor, fontSize = 24.sp, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center)
                    Spacer(Modifier.height(8.dp))
                    Text(
                        text = "-${String.format(java.util.Locale.getDefault(), "%.2f", expense.amount)} €",
                        color = Color(0xFFD95D39),
                        fontSize = 32.sp,
                        fontWeight = FontWeight.ExtraBold
                    )
                }
            }

            Surface(
                color = cardBg,
                shape = RoundedCornerShape(16.dp),
                shadowElevation = 2.dp,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(20.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    DetailRow(AppStrings.get(AppStrings.categoria, appLang), expense.category, textColor, subTextColor)
                    DetailRow(AppStrings.get(AppStrings.mese, appLang), expense.month, textColor, subTextColor)
                    if (expense.date.isNotBlank()) {
                        DetailRow(AppStrings.get(AppStrings.data, appLang), expense.date, textColor, subTextColor)
                    }
                    if (expense.time.isNotBlank()) {
                        DetailRow(AppStrings.get(AppStrings.ora, appLang), expense.time, textColor, subTextColor)
                    }
                    if (expense.description.isNotBlank()) {
                        DetailRow(AppStrings.get(AppStrings.descrizione, appLang), expense.description, textColor, subTextColor)
                    }
                }
            }
            
            Spacer(Modifier.weight(1f))
            
            Button(
                onClick = { onDelete(); onClose() },
                modifier = Modifier.fillMaxWidth().height(56.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD95D39)),
                shape = RoundedCornerShape(16.dp)
            ) {
                Icon(Icons.Default.Delete, contentDescription = null, tint = Color.White)
                Spacer(Modifier.width(8.dp))
                Text(AppStrings.get(AppStrings.elimina, appLang), color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(24.dp))
        }
    }
}

@Composable
fun DetailRow(label: String, value: String, textColor: Color, subTextColor: Color) {
    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
        Text(label, color = subTextColor, fontSize = 16.sp)
        Text(value, color = textColor, fontSize = 16.sp, fontWeight = FontWeight.Medium)
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LanguageSettingsDialog(
    currentLanguage: AppLanguage,
    onLanguageSelected: (AppLanguage) -> Unit,
    onDismiss: () -> Unit
) {
    val appLang = LocalAppLanguage.current
    val isDark = isSystemInDarkTheme()
    val bgColor = if (isDark) Color(0xFF1E1C1A) else Color.White
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(AppStrings.get(AppStrings.lingua, appLang), color = textColor, fontWeight = FontWeight.Bold) },
        text = {
            Column(modifier = Modifier.fillMaxWidth()) {
                AppLanguage.values().forEach { lang ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { 
                                onLanguageSelected(lang)
                                onDismiss()
                            }
                            .padding(vertical = 12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        androidx.compose.material3.RadioButton(
                            selected = currentLanguage == lang,
                            onClick = { 
                                onLanguageSelected(lang)
                                onDismiss()
                            },
                            colors = androidx.compose.material3.RadioButtonDefaults.colors(selectedColor = Terracotta, unselectedColor = Color.Gray)
                        )
                        Spacer(Modifier.width(8.dp))
                        Text(lang.flag, fontSize = 24.sp)
                        Spacer(Modifier.width(8.dp))
                        Text(lang.displayName, color = textColor, fontSize = 16.sp)
                    }
                }
            }
        },
        confirmButton = {
            androidx.compose.material3.TextButton(onClick = onDismiss) {
                Text(AppStrings.get(AppStrings.annulla, appLang), color = Terracotta)
            }
        },
        containerColor = bgColor
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RemindersScreen(
    reminders: List<PaymentReminder>,
    isDark: Boolean,
    onAddReminder: (PaymentReminder) -> Unit,
    onDeleteReminder: (PaymentReminder) -> Unit,
    onPayReminder: (PaymentReminder) -> Unit,
    modifier: Modifier,
    onClose: (() -> Unit)? = null
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
                navigationIcon = {
                    if (onClose != null) {
                        IconButton(onClick = onClose) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = AppStrings.get(AppStrings.indietro, appLang), tint = textColor)
                        }
                    }
                },
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
    val cardBg = if (isDark) Color(0xFF1E1C1A) else Color.White
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
    
    val defaultDate = java.text.SimpleDateFormat("dd/MM/yyyy", java.util.Locale.getDefault()).format(java.util.Date())
    var dueDate by remember { mutableStateOf(defaultDate) }
    var isRecurring by remember { mutableStateOf(false) }
    var maxPaymentsStr by remember { mutableStateOf("") }

    val textColor = if (isDarkTheme) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val dialogBg = if (isDarkTheme) Color(0xFF1D1B18) else Color.White
    val fieldBg = if (isDarkTheme) Color(0xFF2A2724) else Color.White
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
                )
                OutlinedTextField(
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
                }

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

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

if "fun SettingsScreen" not in content:
    content = content + "\n" + screens_code

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Clean screens appended successfully.")
