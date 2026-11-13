import re

with open("src/main/java/it/fm/spese/MainActivity.kt", "r") as f:
    content = f.read()

# 1. Fix SettingsScreen scrolling bug (change Column to LazyColumn)
old_settings_scaffold = """    Scaffold(
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
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Spacer(Modifier.height(8.dp))
            
            SettingsItemRow("""

new_settings_scaffold = """    Scaffold(
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
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item { Spacer(Modifier.height(8.dp)) }
            
            item {
            SettingsItemRow("""

content = content.replace(old_settings_scaffold, new_settings_scaffold)

# Close LazyColumn items in SettingsScreen properly
# We need to wrap each SettingsItemRow in item { ... } or use items.
# Alternatively, since SettingsItemRow has items, let's wrap the block or use item { Column(...) { ... } }
# Let's fix SettingsScreen to use item { Column(...) { ... } } inside LazyColumn to avoid breaking all individual items.

# Let's replace the whole SettingsScreen body with a LazyColumn containing items
settings_screen_body = """    Scaffold(
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
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Spacer(Modifier.height(8.dp))
                Column(verticalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.fillMaxWidth()) {"""

# Replace from Scaffold containerColor in SettingsScreen to the end of SettingsScreen
# Let's target the exact SettingsScreen function definition
print("Refactoring SettingsScreen...")

