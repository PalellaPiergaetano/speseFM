import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Update Dashboard top bar row to include Privacy IconButton next to Settings IconButton
old_dash_header = """                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                    Text(AppStrings.get(AppStrings.panoramica_spese, LocalAppLanguage.current), color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, modifier = Modifier.weight(1f))
                    androidx.compose.material3.IconButton(onClick = onOpenSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = textColor)
                    }
                }"""

new_dash_header = """                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                    Text(AppStrings.get(AppStrings.panoramica_spese, LocalAppLanguage.current), color = textColor, fontSize = 28.sp, fontWeight = FontWeight.ExtraBold, modifier = Modifier.weight(1f))
                    androidx.compose.material3.IconButton(onClick = onTogglePrivacy) {
                        Icon(
                            if (isPrivacyMode) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                            contentDescription = "Privacy",
                            tint = textColor
                        )
                    }
                    androidx.compose.material3.IconButton(onClick = onOpenSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = textColor)
                    }
                }"""

content = content.replace(old_dash_header, new_dash_header)

# 2. Remove Privacy SettingsItemRow from SettingsScreen
privacy_item_row = """                SettingsItemRow(
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
                )"""

content = content.replace(privacy_item_row, "")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Privacy icon moved to Dashboard header and removed from SettingsScreen.")

