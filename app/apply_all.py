import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update AppLanguage and Strings integration
injection = """
enum class AppLanguage(val code: String, val displayName: String, val flag: String) {
    ITALIAN("it", "Italiano", "🇮🇹"),
    ENGLISH("en", "English", "🇬🇧"),
    FRENCH("fr", "Français", "🇫🇷"),
    SPANISH("es", "Español", "🇪🇸")
}
val LocalAppLanguage = androidx.compose.runtime.staticCompositionLocalOf { AppLanguage.ITALIAN }
"""
content = content.replace("enum class AppLanguage(val code: String, val displayName: String, val flag: String) {\n    ITALIAN(\"it\", \"Italiano\", \"🇮🇹\"),\n    ENGLISH(\"en\", \"English\", \"🇬🇧\"),\n    FRENCH(\"fr\", \"Français\", \"🇫🇷\"),\n    SPANISH(\"es\", \"Español\", \"🇪🇸\")\n}", injection)

content = content.replace(
"""@Composable
private fun SpeseAppWithSecurity(
    activity: FragmentActivity,""",
"""@Composable
private fun SpeseAppWithSecurity(
    activity: FragmentActivity,""")


content = content.replace(
"""        SpeseApp(
            onLockClick = { isUnlocked = false },
            launchImport = launchImport,
            launchExport = launchExport
        )""",
"""        val appLang = loadAppLanguage(LocalContext.current)
        androidx.compose.runtime.CompositionLocalProvider(LocalAppLanguage provides appLang) {
            SpeseApp(
                onLockClick = { isUnlocked = false },
                launchImport = launchImport,
                launchExport = launchExport
            )
        }""")

# 2. Fix the Hamburger Menu
drawer_state_code = """
                val drawerState = androidx.compose.material3.rememberDrawerState(initialValue = androidx.compose.material3.DrawerValue.Closed)
                val scope = androidx.compose.runtime.rememberCoroutineScope()

                androidx.compose.material3.ModalNavigationDrawer(
                    drawerState = drawerState,
                    drawerContent = {
                        androidx.compose.material3.ModalDrawerSheet(
                            drawerContainerColor = cardBgColor,
                            drawerContentColor = textColor
                        ) {
                            Spacer(Modifier.height(32.dp))
                            Text("Impostazioni", modifier = Modifier.padding(16.dp), color = textColor, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                            androidx.compose.material3.HorizontalDivider(color = subTextColor.copy(alpha = 0.2f))
                            
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text(if (isPrivacyMode) "Disattiva Privacy" else "Attiva Privacy") },
                                icon = { Icon(if (isPrivacyMode) Icons.Default.VisibilityOff else Icons.Default.Visibility, null) },
                                selected = false,
                                onClick = { kotlinx.coroutines.launch(scope.coroutineContext) { drawerState.close() }; isPrivacyMode = !isPrivacyMode; savePrivacyMode(context, isPrivacyMode) }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Promemoria") },
                                icon = { Icon(Icons.Default.Notifications, null) },
                                selected = false,
                                onClick = { kotlinx.coroutines.launch(scope.coroutineContext) { drawerState.close() }; showRemindersDialog = true }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Lingua") },
                                icon = { Icon(androidx.compose.material.icons.Icons.Default.Language, null) },
                                selected = false,
                                onClick = { kotlinx.coroutines.launch(scope.coroutineContext) { drawerState.close() }; showSettingsDialog = true }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Blocca App") },
                                icon = { Icon(Icons.Default.Lock, null) },
                                selected = false,
                                onClick = { kotlinx.coroutines.launch(scope.coroutineContext) { drawerState.close() }; onLockClick() }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Importa XLS/CSV") },
                                icon = { Icon(Icons.Default.FileUpload, null) },
                                selected = false,
                                onClick = { kotlinx.coroutines.launch(scope.coroutineContext) { drawerState.close() }; launchImport { uri -> 
                                    if (uri != null) {
                                        val imported = XlsSheetImporter.importFromUri(context, uri)
                                        if (imported.isNotEmpty()) {
                                            expenses = imported + expenses
                                            saveExpenses(context, expenses)
                                            Toast.makeText(context, "Importati con successo ${imported.size} movimenti!", Toast.LENGTH_LONG).show()
                                        } else {
                                            Toast.makeText(context, "Nessun movimento valido trovato nel file.", Toast.LENGTH_LONG).show()
                                        }
                                    }
                                } }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Esporta CSV") },
                                icon = { Icon(Icons.Default.FileDownload, null) },
                                selected = false,
                                onClick = { kotlinx.coroutines.launch(scope.coroutineContext) { drawerState.close() }; launchExport("spese_export.csv") { uri -> 
                                    if (uri != null) {
                                        val ok = exportExpensesToCsv(context, uri, expenses)
                                        Toast.makeText(context, if (ok) "Esportazione completata" else "Errore esportazione", Toast.LENGTH_SHORT).show()
                                    }
                                } }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Guida") },
                                icon = { Icon(androidx.compose.material.icons.Icons.Default.Help, null) },
                                selected = false,
                                onClick = { kotlinx.coroutines.launch(scope.coroutineContext) { drawerState.close() }; showTutorial = true }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Svuota Dati") },
                                icon = { Icon(Icons.Default.Delete, null) },
                                selected = false,
                                onClick = { kotlinx.coroutines.launch(scope.coroutineContext) { drawerState.close() }; showClearConfirmDialog = true }
                            )
                        }
                    }
                ) {
                    Scaffold(
                        topBar = {
                            androidx.compose.material3.TopAppBar(
                                title = { Text("Spese FM", fontWeight = FontWeight.Bold, color = textColor) },
                                navigationIcon = {
                                    androidx.compose.material3.IconButton(onClick = { kotlinx.coroutines.launch(scope.coroutineContext) { drawerState.open() } }) {
                                        Icon(androidx.compose.material.icons.Icons.Default.Settings, contentDescription = "Menu", tint = textColor)
                                    }
                                },
                                colors = androidx.compose.material3.TopAppBarDefaults.topAppBarColors(
                                    containerColor = Color.Transparent
                                )
                            )
                        },
                        containerColor = Color.Transparent,"""

content = content.replace("                Scaffold(\n                    containerColor = Color.Transparent,", drawer_state_code)
content = content.replace("                }\n            }\n        }\n    }\n\n    if (showAddDialog)", "                }\n            }\n        }\n        }\n    }\n\n    if (showAddDialog)")

content = re.sub(r'item\s*\{\s*QuickActionsStrip\([\s\S]*?\}\n', '', content)


with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

