import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1 & 2. Expense and PaymentReminder
content = content.replace("data class Expense(\n    val title: String,\n    val category: String,\n    val amount: Double,\n    val date: String\n)", "data class Expense(\n    val title: String,\n    val category: String,\n    val amount: Double,\n    val date: String,\n    val time: String = \"\",\n    val description: String = \"\"\n)")

content = content.replace("data class PaymentReminder(\n    val title: String,\n    val amount: Double,\n    val dueDate: String,\n    val isRecurring: Boolean = false,\n    val recurrenceInterval: String? = null // e.g., \"Mensile\", \"Annuale\"\n)", "data class PaymentReminder(\n    val title: String,\n    val amount: Double,\n    val dueDate: String,\n    val isRecurring: Boolean = false,\n    val recurrenceInterval: String? = null,\n    val maxPayments: Int? = null,\n    val paymentsMade: Int = 0\n)")

# 3. AppLanguage
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

# 4. SpeseAppWithSecurity
security_target = """    val isDarkTheme = isSystemInDarkTheme()
    var isUnlocked by remember { mutableStateOf(false) }"""
security_repl = """    val isDarkTheme = isSystemInDarkTheme()
    var isUnlocked by remember { mutableStateOf(false) }
    var currentLanguage by remember { mutableStateOf(loadAppLanguage(activity)) }
    var showLanguageDialog by remember { mutableStateOf(false) }"""
content = content.replace(security_target, security_repl)

provider_start_target = """        if (!isUnlocked) {"""
provider_start_repl = """        androidx.compose.runtime.CompositionLocalProvider(LocalAppLanguage provides currentLanguage) {
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
        if (!isUnlocked) {"""
content = content.replace(provider_start_target, provider_start_repl)

provider_end_target = """                )
            }
        }
    }
}

@Composable
private fun SpeseApp("""
provider_end_repl = """                )
            }
        }
        }
    }
}

@Composable
private fun SpeseApp("""
content = content.replace(provider_end_target, provider_end_repl)

spese_call_target = """                SpeseApp(
                    onLockClick = {"""
spese_call_repl = """                SpeseApp(
                    onOpenLanguageDialog = { showLanguageDialog = true },
                    onLockClick = {"""
content = content.replace(spese_call_target, spese_call_repl)

# 5. SpeseApp
spese_app_def_target = """private fun SpeseApp(
    onLockClick: () -> Unit,"""
spese_app_def_repl = """private fun SpeseApp(
    onOpenLanguageDialog: () -> Unit,
    onLockClick: () -> Unit,"""
content = content.replace(spese_app_def_target, spese_app_def_repl)

spese_app_state_target = """    var showClearConfirmDialog by remember { mutableStateOf(false) }"""
spese_app_state_repl = """    var showClearConfirmDialog by remember { mutableStateOf(false) }
    var showSettings by remember { mutableStateOf(false) }
    var selectedExpense by remember { mutableStateOf<Expense?>(null) }"""
content = content.replace(spese_app_state_target, spese_app_state_repl)

# Routing in SpeseApp
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

# Close `else {` of Scaffold
spese_app_close_route_target = """                }
            }
        }
    }
}

@Composable
private fun Dashboard("""
spese_app_close_route_repl = """                }
                }
            }
        }
    }
}

@Composable
private fun Dashboard("""
content = content.replace(spese_app_close_route_target, spese_app_close_route_repl)

# 7 & 8. Dashboard adjustments
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
                    IconButton(onClick = onOpenSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = textColor)
                    }
                }
            }"""
content = content.replace(panoramica_target, panoramica_repl)

# Remove QuickActionsStrip from Dashboard
content = re.sub(r'item\s*\{\s*QuickActionsStrip\(.*?\}\n\n\s*if \(!isPrivacyMode\)', r'if (!isPrivacyMode)', content, flags=re.DOTALL)

# 9. Movements adjustments
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

# 10. ExpenseRow clickable
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

# Fix ExpenseRow calls
content = content.replace("onDelete = { onDeleteExpense(e) }\n                    )", "onClick = { onExpenseClick(e) },\n                        onDelete = { onDeleteExpense(e) }\n                    )")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

