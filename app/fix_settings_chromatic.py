import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Update SettingsScreen to include BackgroundCircles and matching cardBg
old_settings_scaffold = """    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
    val appLang = LocalAppLanguage.current
    val cardBg = if (isDark) Color(0xFF2A2724) else Color.White

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
    ) { padding ->"""

new_settings_scaffold = """    val textColor = if (isDark) Color(0xFFF3EFEA) else Color(0xFF1E1B18)
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
        ) { padding ->"""

content = content.replace(old_settings_scaffold, new_settings_scaffold)

# Close the Box in SettingsScreen
# SettingsScreen ends with `    }\n}\n\n@Composable`
old_settings_end = """        }
    }
}


@Composable
fun SettingsItemRow("""

new_settings_end = """        }
    }
    }
}


@Composable
fun SettingsItemRow("""

content = content.replace(old_settings_end, new_settings_end)

# Update SettingsItemRow to use Terracotta / app accent color instead of hardcoded Violet
old_row_icon = """            Box(
                modifier = Modifier
                    .size(40.dp)
                    .background(Color(0xFF6C5CE7).copy(alpha = 0.1f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(icon, contentDescription = title, tint = Color(0xFF6C5CE7))
            }"""

new_row_icon = """            Box(
                modifier = Modifier
                    .size(40.dp)
                    .background(Terracotta.copy(alpha = 0.15f), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(icon, contentDescription = title, tint = Terracotta)
            }"""

content = content.replace(old_row_icon, new_row_icon)

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

print("Settings chromatic consistency applied successfully.")

