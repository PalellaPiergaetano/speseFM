import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

idx = content.find("data class TutorialStep")
# Add two `}` before it to close ModalNavigationDrawer and CompositionLocalProvider
# `before` was `}\n            }\n        )\n    }\n}`
# But `LanguageSettingsDialog` call is now right before `TutorialStep`! Oh, I see. `LanguageSettingsDialog` is inside `SpeseApp`.
# In `add_dialog_call.py` I added:
# if (showSettingsDialog) { LanguageSettingsDialog(...) }
# Wait, let's just make sure SpeseApp is properly closed.

# Add 2 closing braces at the end of SpeseApp
content = content.replace(
"""        )
    }
}""",
"""        )
    }
    }
    }
}""")

# What about `saveAppLanguage(context, lang)` -> Unresolved reference context?
# In `LanguageSettingsDialog` inside SpeseApp, `context` is `LocalContext.current`
content = content.replace("Toast.makeText(context, \"Lingua aggiornata\", Toast.LENGTH_SHORT).show()", "Toast.makeText(context, AppStrings.get(AppStrings.lingua_impostata_lang_displayname, LocalAppLanguage.current).replace(\"${lang.displayName}\", lang.displayName), Toast.LENGTH_SHORT).show()")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

