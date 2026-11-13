import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# I will replace all `appLanguage` used inside `AppStrings.get(...)` with a local variable `val appLanguage = LocalAppLanguage.current` at the beginning of Composables or pass it.
# Actually, the easiest fix is just changing `AppStrings.get(AppStrings.something, appLanguage)` to `AppStrings.get(AppStrings.something, LocalAppLanguage.current)`.
# But wait, `Toast` isn't a Composable, so it can't use `LocalAppLanguage.current`. Let's see where the errors are.

errors = [
    680, 1136, 1225, 1385, 1468, 1499, 1536, 1566, 1592, 1593, 1618, 1619, 1644, 1645, 1670, 1671, 1696, 1697,
    1722, 1723, 1748, 1749, 1944, 2018, 2066, 2067, 2080, 2179, 2180, 2338, 2339, 2388, 2408, 2438, 2543, 2822,
    2848, 2859, 2880, 2894, 2931, 2974, 2989, 3004, 3016, 3028, 3133, 3178, 3200, 3205, 3248, 3265, 3317, 3336,
    3351, 3366, 3381, 3394, 3423, 3450, 3459, 3492, 3544
]

lines = content.split("\n")
for line_num in errors:
    idx = line_num - 1
    # Se la linea è dentro un Composable, possiamo usare LocalAppLanguage.current
    # Sostituiamo ', appLanguage)' con ', LocalAppLanguage.current)' in quelle righe.
    lines[idx] = lines[idx].replace(', appLanguage)', ', LocalAppLanguage.current)')

# Aggiungiamo LocalAppLanguage in alto
if "val LocalAppLanguage" not in content:
    import_statement = "import androidx.compose.runtime.staticCompositionLocalOf\n\nval LocalAppLanguage = staticCompositionLocalOf { AppLanguage.ITALIAN }\n"
    # Find the enum class AppLanguage and put it after
    for i, line in enumerate(lines):
        if "enum class AppLanguage" in line:
            lines.insert(i-1, import_statement)
            break

# E poi mettiamo CompositionLocalProvider dentro SpeseApp
# `SpeseApp` is defined at `fun SpeseApp`
# We can find `Scaffold` inside `SpeseApp` and wrap it? No, `SpeseApp` uses `CompositionLocalProvider`.
# Actually, I can just write a wrapper.

new_content = "\n".join(lines)
with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(new_content)

