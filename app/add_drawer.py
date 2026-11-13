import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Trovo l'inizio di Scaffold e ci metto il drawer.
# Prima devo definire il DrawerState.
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
                            Divider(color = subTextColor.copy(alpha = 0.2f))
                            
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text(if (isPrivacyMode) "Disattiva Privacy" else "Attiva Privacy") },
                                icon = { Icon(if (isPrivacyMode) Icons.Default.VisibilityOff else Icons.Default.Visibility, null) },
                                selected = false,
                                onClick = { scope.launch { drawerState.close() }; onTogglePrivacy() }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Promemoria") },
                                icon = { Icon(Icons.Default.Notifications, null) },
                                selected = false,
                                onClick = { scope.launch { drawerState.close() }; showRemindersDialog = true }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Lingua") },
                                icon = { Icon(Icons.Default.Language, null) },
                                selected = false,
                                onClick = { scope.launch { drawerState.close() }; showSettingsDialog = true }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Blocca App") },
                                icon = { Icon(Icons.Default.Lock, null) },
                                selected = false,
                                onClick = { scope.launch { drawerState.close() }; onLockClick() }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Importa XLS/CSV") },
                                icon = { Icon(Icons.Default.FileUpload, null) },
                                selected = false,
                                onClick = { scope.launch { drawerState.close() }; launchImport { uri -> 
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
                                onClick = { scope.launch { drawerState.close() }; launchExport("spese_export.csv") { uri -> 
                                    if (uri != null) {
                                        val ok = exportExpensesToCsv(context, uri, expenses)
                                        Toast.makeText(context, if (ok) "Esportazione completata" else "Errore esportazione", Toast.LENGTH_SHORT).show()
                                    }
                                } }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Guida") },
                                icon = { Icon(Icons.Default.Help, null) },
                                selected = false,
                                onClick = { scope.launch { drawerState.close() }; showTutorial = true }
                            )
                            androidx.compose.material3.NavigationDrawerItem(
                                label = { Text("Svuota Dati") },
                                icon = { Icon(Icons.Default.Delete, null) },
                                selected = false,
                                onClick = { scope.launch { drawerState.close() }; showClearConfirmDialog = true }
                            )
                        }
                    }
                ) {
                    Scaffold(
                        topBar = {
                            androidx.compose.material3.TopAppBar(
                                title = { Text("Spese FM", fontWeight = FontWeight.Bold, color = textColor) },
                                navigationIcon = {
                                    androidx.compose.material3.IconButton(onClick = { scope.launch { drawerState.open() } }) {
                                        Icon(Icons.Default.Menu, contentDescription = "Menu", tint = textColor)
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

# Fix launchImport that was inside QuickActionsStrip. 
# Wait, launchImport is passed to Dashboard. 
# We remove QuickActionsStrip from Dashboard.
# Find `item { QuickActionsStrip(` inside Dashboard and remove it.

# In Dashboard:
# Remove lines from `item {` of QuickActionsStrip to `)` of its end.
import re
content = re.sub(r'item\s*\{\s*QuickActionsStrip\([\s\S]*?\}\n', '', content)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

