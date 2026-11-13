import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add showSettings state in SpeseApp
content = content.replace("var showBudgetDialog by remember { mutableStateOf(false) }", "var showBudgetDialog by remember { mutableStateOf(false) }\n    var showSettings by remember { mutableStateOf(false) }")

# Update Dashboard call to handle onOpenSettingsClick
dash_call_target = """onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            modifier = Modifier.padding(innerPadding)
                        )"""
dash_call_repl = """onDeleteExpense = { e -> expenses = expenses.filter { it != e }; saveExpenses(context, expenses) },
                            onOpenSettingsClick = { showSettings = true },
                            modifier = Modifier.padding(innerPadding)
                        )"""
content = content.replace(dash_call_target, dash_call_repl)

# Add SettingsScreen code
settings_code = """
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
                    Switch(checked = isPrivacyMode, onCheckedChange = { onTogglePrivacy() })
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
"""

if "fun SettingsScreen" not in content:
    content = content + "\n" + settings_code

# Display SettingsScreen in SpeseApp
show_settings_logic = """
            if (showSettings) {
                SettingsScreen(
                    isDark = isDark,
                    isPrivacyMode = isPrivacyMode,
                    onTogglePrivacy = { 
                        isPrivacyMode = !isPrivacyMode
                        savePrivacyMode(context, isPrivacyMode)
                    },
                    onLockClick = onLockClick,
                    onImportClick = { launchImport { uri -> uri?.let { importXlsToExpenses(context, it) { newExp -> expenses = expenses + newExp; saveExpenses(context, expenses) } } } },
                    onExportClick = { launchExport("Spese_FM_Backup_${System.currentTimeMillis()}.csv") { uri -> uri?.let { exportCsv(context, it, expenses) } } },
                    onClearAllClick = { showClearConfirmDialog = true },
                    onOpenTutorialClick = { showTutorial = true; showSettings = false },
                    onLanguageClick = { /* We will add LanguageSettingsDialog */ },
                    onClose = { showSettings = false }
                )
            } else {
                Scaffold(
"""

content = content.replace("Scaffold(\n                    containerColor = Color.Transparent,", show_settings_logic + "                    containerColor = Color.Transparent,")

# Add another } at the end of SpeseApp to close the else block
spese_app_end_target = """                }
            }
        }
    }
}"""
spese_app_end_repl = """                }
                }
            }
        }
    }
}"""
content = content.replace(spese_app_end_target, spese_app_end_repl)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

