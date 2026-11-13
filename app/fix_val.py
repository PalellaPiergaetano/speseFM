import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# Fix the one in Dashboard (line 1405) back to onTogglePrivacy()
# Find clickable { isPrivacyMode = !isPrivacyMode; savePrivacyMode(context, isPrivacyMode); Toast.makeText(context, if (isPrivacyMode) "Privacy attivata" else "Privacy disattivata", Toast.LENGTH_SHORT).show() }
# Replace it with clickable { onTogglePrivacy() }
# Wait, actually, the one in Dashboard is EXACTLY this.
content = content.replace("modifier = Modifier.clip(RoundedCornerShape(20.dp)).clickable { isPrivacyMode = !isPrivacyMode; savePrivacyMode(context, isPrivacyMode); Toast.makeText(context, if (isPrivacyMode) \"Privacy attivata\" else \"Privacy disattivata\", Toast.LENGTH_SHORT).show() }", "modifier = Modifier.clip(RoundedCornerShape(20.dp)).clickable { onTogglePrivacy() }")

# Let's fix conflicting import ExperimentalMaterial3Api
content = content.replace("import androidx.compose.material3.ExperimentalMaterial3Api\nimport androidx.compose.material3.ExperimentalMaterial3Api\n", "import androidx.compose.material3.ExperimentalMaterial3Api\n")

with open("src/main/java/it/fm/spese/MainActivity.kt", "w") as f:
    f.write(content)

