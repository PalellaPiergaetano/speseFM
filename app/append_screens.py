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
                    IconButton(onClick = onClose) {
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
                    IconButton(onClick = onClose) {
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
                        text = "-${String.format(Locale.getDefault(), "%.2f", expense.amount)} €",
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
            TextButton(onClick = onDismiss) {
                Text(AppStrings.get(AppStrings.annulla, appLang), color = Terracotta)
            }
        },
        containerColor = bgColor
    )
}
"""

if "fun SettingsScreen" not in content:
    content = content + "\n" + screens_code

# I also need to import `androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight`
# and `androidx.compose.material.icons.filled.Settings`
# and `androidx.compose.material.icons.automirrored.filled.ArrowBack`
# and `androidx.compose.material.icons.filled.Language`
imports_to_add = """
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Language
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.Switch
import androidx.compose.material3.RadioButton
import androidx.compose.material3.RadioButtonDefaults
"""
if "import androidx.compose.material.icons.filled.Settings" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Add", imports_to_add + "import androidx.compose.material.icons.filled.Add")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

