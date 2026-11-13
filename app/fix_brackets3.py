import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("    }\n    }\n    }\n}\n\nprivate fun launchBiometricPrompt(", "    }\n}\n\nprivate fun launchBiometricPrompt(")
content = content.replace("Icon(androidx.compose.material.icons.Icons.Default.Settings", "Icon(androidx.compose.material.icons.Icons.Default.Settings")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

