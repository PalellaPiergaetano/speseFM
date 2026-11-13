import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix CompositionLocalProvider
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
repl_sec = """    androidx.compose.runtime.CompositionLocalProvider(LocalAppLanguage provides currentLanguage) {
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

if target_sec in content:
    content = content.replace(target_sec, repl_sec)
else:
    print("Could not find SpeseAppWithSecurity target!")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

