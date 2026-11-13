import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Replace Panoramica Spese row with one having a Settings icon
target = """                Text("Panoramica Spese", color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold)
            }"""
            
replacement = """                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                    Text(AppStrings.get(AppStrings.panoramica_spese, appLang), color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, modifier = Modifier.weight(1f))
                    IconButton(onClick = onOpenSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = textColor)
                    }
                }
            }"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("Could not find Panoramica Spese!")

# Update Dashboard signature to include onOpenSettingsClick
dash_target = "onDeleteExpense: (Expense) -> Unit,"
dash_repl = "onDeleteExpense: (Expense) -> Unit,\n    onOpenSettingsClick: () -> Unit,"
if dash_target in content:
    content = content.replace(dash_target, dash_repl)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

