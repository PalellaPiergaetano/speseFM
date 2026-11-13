import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Add LanguageSettingsDialog code
lang_dialog_code = """
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LanguageSettingsDialog(
    currentLanguage: AppLanguage,
    onLanguageSelected: (AppLanguage) -> Unit,
    onDismiss: () -> Unit
) {
    val context = LocalContext.current
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
                        RadioButton(
                            selected = currentLanguage == lang,
                            onClick = { 
                                onLanguageSelected(lang)
                                onDismiss()
                            },
                            colors = RadioButtonDefaults.colors(selectedColor = Terracotta, unselectedColor = Color.Gray)
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
if "fun LanguageSettingsDialog" not in content:
    content = content + "\n" + lang_dialog_code

# Display LanguageSettingsDialog
show_lang_dialog_logic = """
    var showLanguageDialog by remember { mutableStateOf(false) }
    var currentLanguage by remember { mutableStateOf(loadAppLanguage(context)) }

    // Wrap the entire app content inside CompositionLocalProvider
"""

# Let's insert the composition local provider and the language dialog state
# In SpeseAppWithSecurity:
spese_app_sec_target = """        var isUnlocked by remember { mutableStateOf(!isPrivacyMode) }

        if (!isUnlocked) {"""
spese_app_sec_repl = """        var isUnlocked by remember { mutableStateOf(!isPrivacyMode) }
        var currentLanguage by remember { mutableStateOf(loadAppLanguage(context)) }
        var showLanguageDialog by remember { mutableStateOf(false) }

        androidx.compose.runtime.CompositionLocalProvider(LocalAppLanguage provides currentLanguage) {
            if (showLanguageDialog) {
                LanguageSettingsDialog(
                    currentLanguage = currentLanguage,
                    onLanguageSelected = { 
                        currentLanguage = it
                        saveAppLanguage(context, it)
                    },
                    onDismiss = { showLanguageDialog = false }
                )
            }

        if (!isUnlocked) {"""

content = content.replace(spese_app_sec_target, spese_app_sec_repl)

# Close the CompositionLocalProvider at the end of SpeseAppWithSecurity
spese_app_sec_end_target = """                )
            }
        }
    }
}

// ==========================================
// SpeseApp (Main App)"""
spese_app_sec_end_repl = """                )
            }
        }
        }
    }
}

// ==========================================
// SpeseApp (Main App)"""
content = content.replace(spese_app_sec_end_target, spese_app_sec_end_repl)

# Now wire LanguageSettingsDialog logic into SettingsScreen
# In SettingsScreen we have onLanguageClick
# We need to trigger showLanguageDialog = true from SettingsScreen
# SettingsScreen is called from SpeseApp. So SpeseApp needs onOpenLanguageDialog
# But wait, SpeseApp is called from SpeseAppWithSecurity.
spese_app_call_target = """                SpeseApp(
                    onLockClick = {
                        isPrivacyMode = true
                        isUnlocked = false
                        savePrivacyMode(context, true)
                    },"""
spese_app_call_repl = """                SpeseApp(
                    onOpenLanguageDialog = { showLanguageDialog = true },
                    onLockClick = {
                        isPrivacyMode = true
                        isUnlocked = false
                        savePrivacyMode(context, true)
                    },"""
content = content.replace(spese_app_call_target, spese_app_call_repl)

spese_app_def_target = """private fun SpeseApp(
    onLockClick: () -> Unit,"""
spese_app_def_repl = """private fun SpeseApp(
    onOpenLanguageDialog: () -> Unit,
    onLockClick: () -> Unit,"""
content = content.replace(spese_app_def_target, spese_app_def_repl)

spese_app_settings_call_target = "onLanguageClick = { /* We will add LanguageSettingsDialog */ },"
spese_app_settings_call_repl = "onLanguageClick = onOpenLanguageDialog,"
content = content.replace(spese_app_settings_call_target, spese_app_settings_call_repl)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

