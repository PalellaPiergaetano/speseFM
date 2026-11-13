import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update Expense and PaymentReminder
content = content.replace("data class Expense(\n    val title: String,\n    val category: String,\n    val amount: Double,\n    val date: String\n)", "data class Expense(\n    val title: String,\n    val category: String,\n    val amount: Double,\n    val date: String,\n    val time: String = \"\",\n    val description: String = \"\"\n)")
content = content.replace("data class PaymentReminder(\n    val title: String,\n    val amount: Double,\n    val dueDate: String,\n    val isRecurring: Boolean = false,\n    val recurrenceInterval: String? = null // e.g., \"Mensile\", \"Annuale\"\n)", "data class PaymentReminder(\n    val title: String,\n    val amount: Double,\n    val dueDate: String,\n    val isRecurring: Boolean = false,\n    val recurrenceInterval: String? = null,\n    val maxPayments: Int? = null,\n    val paymentsMade: Int = 0\n)")

# 2. Add AppLanguage definition
lang_def = """
enum class AppLanguage(val code: String, val displayName: String, val flag: String) {
    ITALIAN("it", "Italiano", "🇮🇹"),
    ENGLISH("en", "English", "🇬🇧"),
    FRENCH("fr", "Français", "🇫🇷"),
    SPANISH("es", "Español", "🇪🇸")
}

val LocalAppLanguage = androidx.compose.runtime.staticCompositionLocalOf { AppLanguage.ITALIAN }

fun loadAppLanguage(context: Context): AppLanguage {
    val prefs = context.getSharedPreferences("app_settings", Context.MODE_PRIVATE)
    val code = prefs.getString("language_code", "it") ?: "it"
    return AppLanguage.values().find { it.code == code } ?: AppLanguage.ITALIAN
}

fun saveAppLanguage(context: Context, language: AppLanguage) {
    val prefs = context.getSharedPreferences("app_settings", Context.MODE_PRIVATE)
    prefs.edit().putString("language_code", language.code).apply()
}

"""
content = content.replace("private val Violet = Color(0xFF6C5CE7)", "private val Violet = Color(0xFF6C5CE7)\n" + lang_def)

# 3. Fix SpeseAppWithSecurity
target_sec = """    if (!isUnlocked) {
        SecurityLockOverlay(
            isDarkTheme = isDarkTheme,
            onUnlockClick = { triggerBiometric() }
        )
    } else {
        SpeseApp(
            onLockClick = { isUnlocked = false },
            launchImport = launchImport,
            launchExport = launchExport
        )
    }
}"""
repl_sec = """    var currentLanguage by remember { mutableStateOf(loadAppLanguage(activity)) }
    var showLanguageDialog by remember { mutableStateOf(false) }

    androidx.compose.runtime.CompositionLocalProvider(LocalAppLanguage provides currentLanguage) {
        if (showLanguageDialog) {
            LanguageSettingsDialog(
                currentLanguage = currentLanguage,
                onLanguageSelected = { 
                    currentLanguage = it
                    saveAppLanguage(activity, it)
                },
                onDismiss = { showLanguageDialog = false }
            )
        }
        if (!isUnlocked) {
            SecurityLockOverlay(
                isDarkTheme = isDarkTheme,
                onUnlockClick = { triggerBiometric() }
            )
        } else {
            SpeseApp(
                onOpenLanguageDialog = { showLanguageDialog = true },
                onLockClick = { isUnlocked = false },
                launchImport = launchImport,
                launchExport = launchExport
            )
        }
    }
}"""
content = content.replace(target_sec, repl_sec)

# 4. SpeseApp Definition
content = content.replace("private fun SpeseApp(\n    onLockClick: () -> Unit,", "private fun SpeseApp(\n    onOpenLanguageDialog: () -> Unit,\n    onLockClick: () -> Unit,")

spese_app_state_target = """    var showClearConfirmDialog by remember { mutableStateOf(false) }"""
spese_app_state_repl = """    var showClearConfirmDialog by remember { mutableStateOf(false) }
    var showSettings by remember { mutableStateOf(false) }
    var selectedExpense by remember { mutableStateOf<Expense?>(null) }"""
content = content.replace(spese_app_state_target, spese_app_state_repl)

# 5. Routing inside SpeseApp
spese_app_route_target = """            Box(modifier = Modifier.fillMaxSize().background(paperColor)) {
                BackgroundCircles(isDarkTheme)

                Scaffold("""
spese_app_route_repl = """            Box(modifier = Modifier.fillMaxSize().background(paperColor)) {
                BackgroundCircles(isDarkTheme)

                if (selectedExpense != null) {
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
                } else if (showSettings) {
                    SettingsScreen(
                        isDark = isDarkTheme,
                        isPrivacyMode = isPrivacyMode,
                        onTogglePrivacy = { 
                            isPrivacyMode = !isPrivacyMode
                            savePrivacyMode(context, isPrivacyMode)
                        },
                        onLockClick = onLockClick,
                        onImportClick = { launchImport { uri -> uri?.let { importXlsToExpenses(context, it) { newExp -> expenses = expenses + newExp; saveExpenses(context, expenses) } } } },
                        onExportClick = { launchExport("Spese_FM_Backup.csv") { uri -> uri?.let { exportCsv(context, it, expenses) } } },
                        onClearAllClick = { showClearConfirmDialog = true },
                        onOpenTutorialClick = { showTutorial = true; showSettings = false },
                        onLanguageClick = onOpenLanguageDialog,
                        onClose = { showSettings = false }
                    )
                } else {
                Scaffold("""
content = content.replace(spese_app_route_target, spese_app_route_repl)

# Close `else` branch of Scaffold inside SpeseApp
close_target = """        )
    }
}

data class TutorialStep("""
close_repl = """        )
    }
}
} // Closes the `else` branch for Scaffold

data class TutorialStep("""
content = content.replace(close_target, close_repl)

# 6. Dashboard adjustments
dash_def_target = """    onDeleteExpense: (Expense) -> Unit,
    modifier: Modifier
)"""
dash_def_repl = """    onDeleteExpense: (Expense) -> Unit,
    onOpenSettingsClick: () -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
)"""
content = content.replace(dash_def_target, dash_def_repl)

dash_call_target = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            modifier = Modifier.padding(innerPadding)
                        )"""
dash_call_repl = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            onOpenSettingsClick = { showSettings = true },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(innerPadding)
                        )"""
content = content.replace(dash_call_target, dash_call_repl)

# Settings Icon in Dashboard
panoramica_target = """                Text("Panoramica Spese", color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
            }"""
panoramica_repl = """                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                    Text(AppStrings.get(AppStrings.panoramica_spese, LocalAppLanguage.current), color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, modifier = Modifier.weight(1f))
                    androidx.compose.material3.IconButton(onClick = onOpenSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = textColor)
                    }
                }
            }"""
content = content.replace(panoramica_target, panoramica_repl)

# Remove QuickActionsStrip from Dashboard
content = re.sub(r'item\s*\{\s*QuickActionsStrip\(.*?\}\n\n\s*if \(!isPrivacyMode\)', r'if (!isPrivacyMode)', content, flags=re.DOTALL)

# 7. Movements adjustments
mov_def_target = """    onDeleteExpense: (Expense) -> Unit,
    modifier: Modifier
)"""
mov_def_repl = """    onDeleteExpense: (Expense) -> Unit,
    onExpenseClick: (Expense) -> Unit,
    modifier: Modifier
)"""
content = content.replace(mov_def_target, mov_def_repl)

mov_call_target = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            modifier = Modifier.padding(innerPadding)
                        )"""
mov_call_repl = """                            onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            onExpenseClick = { selectedExpense = it },
                            modifier = Modifier.padding(innerPadding)
                        )"""
content = content.replace(mov_call_target, mov_call_repl)

# 8. ExpenseRow clickable
row_def_target = """fun ExpenseRow(
    expense: Expense,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onDelete: () -> Unit
)"""
row_def_repl = """fun ExpenseRow(
    expense: Expense,
    isDark: Boolean,
    isPrivacyMode: Boolean,
    onClick: () -> Unit,
    onDelete: () -> Unit
)"""
content = content.replace(row_def_target, row_def_repl)

row_surf_target = """        shape = RoundedCornerShape(16.dp),
        shadowElevation = 2.dp,
        modifier = Modifier.fillMaxWidth()
    ) {"""
row_surf_repl = """        shape = RoundedCornerShape(16.dp),
        shadowElevation = 2.dp,
        modifier = Modifier.fillMaxWidth().clickable { onClick() }
    ) {"""
content = content.replace(row_surf_target, row_surf_repl)

# Fix ExpenseRow calls in Dashboard and Movements
content = content.replace("onDelete = { onDeleteExpense(e) }\n                    )", "onClick = { onExpenseClick(e) },\n                        onDelete = { onDeleteExpense(e) }\n                    )")

# 9. Append missing components
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
    onClose: () -> Unit
) {
    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val cardBg = if (isDark) Color(0xFF2A2724) else Color.White
    val appLang = LocalAppLanguage.current

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
        containerColor = if (isDark) Color(0xFF121110) else Color(0xFFFAF7F2)
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 20.dp),
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
                    .background(Color(0xFF6C5CE7).copy(alpha = 0.1f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(icon, contentDescription = title, tint = Color(0xFF6C5CE7))
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
    val cardBg = if (isDark) Color(0xFF2A2724) else Color.White
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
                    val catInfo = mapColumnToCategory(expense.category)
                    Box(
                        modifier = Modifier
                            .size(64.dp)
                            .background(catInfo.color.copy(alpha = 0.2f), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(catInfo.emoji, fontSize = 32.sp)
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
                    DetailRow(AppStrings.get(AppStrings.data, appLang), expense.date, textColor, subTextColor)
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
"""
content = content + "\n" + screens_code

# Add necessary imports
imports = """
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.HelpOutline
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.Switch
import androidx.compose.material3.RadioButton
import androidx.compose.material3.RadioButtonDefaults
"""
if "import androidx.compose.material.icons.automirrored.filled.ArrowBack" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Add", imports.strip() + "\nimport androidx.compose.material.icons.filled.Add")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

