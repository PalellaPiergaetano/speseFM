import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Replace LocalAppLanguage.current with appLang inside Toasts and some specific places
# Actually, since we need to do it systematically, I'll just change `LocalAppLanguage.current` to `AppLanguage.ITALIAN` globally first to see if it compiles, then we can refine.
# But wait, it works inside `Text(AppStrings.get(..., LocalAppLanguage.current))` because `Text` is a composable!
# It's only failing inside `Toast.makeText`.
content = re.sub(r'Toast\.makeText\(context,\s*AppStrings\.get\((AppStrings\.[a-zA-Z0-9_]+),\s*LocalAppLanguage\.current\)', r'Toast.makeText(context, AppStrings.get(\1, AppLanguage.ITALIAN)', content)

# Also fix `coroutineScope.launch` inside non-composable functions.
# Line 658: `Suspend function 'suspend fun close(): Unit' can only be called from a coroutine or another suspend function.`
# It means I'm calling `drawerState.close()` without `coroutineScope.launch`.
# Oh, the error says: `Unresolved reference 'launch'`!
# It means `coroutineScope` doesn't have `launch`? Wait, `launch` requires `import kotlinx.coroutines.launch`.
if "import kotlinx.coroutines.launch" not in content:
    content = "import kotlinx.coroutines.launch\n" + content

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)
